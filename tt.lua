local dap = require('dap')
local dapui = require('dapui')

-- Setup dap-ui
dapui.setup()

-- Lua Debug Adapter Configuration with mobdebug
dap.adapters.lua = {
  type = 'server',
  host = '127.0.0.1',
  port = 8172,  -- Default port for mobdebug
}

dap.configurations.lua = {
  {
    type = 'lua',
    request = 'launch',
    name = 'Launch Lua file with mobdebug',
    program = function()
      return vim.fn.input('Path to Lua script: ', vim.fn.getcwd() .. '/', 'file')  -- Choose Lua script to debug
    end,
    stopOnEntry = true,
    cwd = vim.fn.getcwd(),  -- Current working directory
    externalConsole = false,
  },
}

-- Optionally open dap-ui on start
dap.listeners.after['event_initialized']['dapui_config'] = function()
  dapui.open()
end

dap.listeners.before['event_terminated']['dapui_config'] = function()
  dapui.close()
end

dap.listeners.before['event_exited']['dapui_config'] = function()
  dapui.close()
end
