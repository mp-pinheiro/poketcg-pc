local required_domains = {
  "WRAM", "ROM", "VRAM", "OAM", "HRAM", "CartRAM", "System Bus"
}
local required_registers = { "A", "F", "B", "C", "D", "E", "H", "L", "SP", "PC" }

local function fail(message)
  error("UNSUPPORTED_CAPABILITY " .. message, 0)
end

local function json_string(value)
  value = tostring(value)
  value = value:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", "\\n")
  return '"' .. value .. '"'
end

local function json_value(value)
  if type(value) == "string" then
    return json_string(value)
  elseif type(value) == "number" then
    return tostring(value)
  elseif type(value) == "boolean" then
    return value and "true" or "false"
  elseif type(value) ~= "table" then
    return "null"
  end
  local is_array = true
  local maximum = 0
  for key, _ in pairs(value) do
    if type(key) ~= "number" or key < 1 or key % 1 ~= 0 then
      is_array = false
      break
    end
    maximum = math.max(maximum, key)
  end
  local result = {}
  if is_array then
    for index = 1, maximum do
      result[index] = json_value(value[index])
    end
    return "[" .. table.concat(result, ",") .. "]"
  end
  for key, item in pairs(value) do
    result[#result + 1] = json_string(key) .. ":" .. json_value(item)
  end
  return "{" .. table.concat(result, ",") .. "}"
end

local function json_array(values)
  return json_value(values)
end

local function json_object(values)
  return json_value(values)
end

local function list_values(value)
  local result = {}
  if type(value) == "string" then
    for item in value:gmatch("[^\r\n]+") do
      result[#result + 1] = item
    end
  elseif type(value) == "table" then
    for _, item in pairs(value) do
      result[#result + 1] = tostring(item)
    end
  end
  return result
end

local function contains(values, wanted)
  for _, value in ipairs(values) do
    if value == wanted then
      return true
    end
  end
  return false
end

local function hex_bytes(values)
  local result = {}
  for index, value in ipairs(values) do
    result[index] = string.format("%02x", value)
  end
  return table.concat(result)
end

local domains = list_values(memory.getmemorydomainlist())
for _, wanted in ipairs(required_domains) do
  if not contains(domains, wanted) then
    fail("memory-domain=" .. wanted)
  end
end

local registers = emu.getregisters()
if type(registers) ~= "table" then
  fail("register-table")
end
for _, wanted in ipairs(required_registers) do
  if registers[wanted] == nil and registers[string.lower(wanted)] == nil then
    fail("register=" .. wanted)
  end
end

local scopes = list_values(event.availableScopes())
local bus_scope = nil
for _, scope in ipairs(scopes) do
  if string.lower(scope):find("bus", 1, true) then
    bus_scope = scope
    break
  end
end
if not bus_scope then
  fail("bus-execution-scope")
end

local trace = {}
local anchor = tonumber(os.getenv("POKETCG_BIZHAWK_ANCHOR_ADDR") or "0x0150")
local callback = event.on_bus_exec(function(address, value, flags)
  trace[#trace + 1] = { address = address, value = value, flags = flags }
end, anchor, "poketcg-completion", bus_scope)
if callback == nil then
  fail("bus-execution-hook")
end

local frames = tonumber(os.getenv("POKETCG_BIZHAWK_FRAMES") or "1")
if not frames or frames < 1 then
  fail("frame-bound")
end
local input_rle = {}
for frame = 1, frames do
  joypad.set({ A = false, B = false, Select = false, Start = false,
               Right = false, Left = false, Up = false, Down = false })
  emu.frameadvance()
  local last = input_rle[#input_rle]
  if last and last.buttons == 0 then
    last.frames = last.frames + 1
  else
    input_rle[#input_rle + 1] = { buttons = 0, frames = 1 }
  end
end

local raw_domains = {}
for _, domain in ipairs(required_domains) do
  local size = memory.getmemorydomainsize(domain)
  if not size or size < 1 then
    fail("empty-memory-domain=" .. domain)
  end
  raw_domains[domain] = hex_bytes(memory.read_bytes_as_array(0, size, domain))
end

local screenshot = os.getenv("POKETCG_BIZHAWK_SCREENSHOT")
if not screenshot or screenshot == "" then
  fail("screenshot-path")
end
client.screenshot(screenshot)

local output = os.getenv("POKETCG_BIZHAWK_OUTPUT")
if not output or output == "" then
  fail("output-path")
end
local record = {
  schema = 1,
  format = "bizhawk-raw-v1",
  scenario = os.getenv("POKETCG_BIZHAWK_SCENARIO") or "unknown",
  rom_sha256 = os.getenv("POKETCG_BIZHAWK_ROM_SHA256") or "",
  frames = frames,
  input_rle = input_rle,
  domains = raw_domains,
  registers = registers,
  trace = trace,
  bus_scope = bus_scope,
  screenshot = screenshot,
}
local file = assert(io.open(output, "wb"))
file:write(json_object(record))
file:close()
