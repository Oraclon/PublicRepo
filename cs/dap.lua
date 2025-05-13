local M = {
	"mfussenegger/nvim-dap",
}
M.dependencies = {
	"rcarriga/nvim-dap-ui",
	"nvim-neotest/nvim-nio",
	"Cliffback/netcoredbg-macOS-arm64.nvim",
	"nvim-lua/plenary.nvim",
}

M.config = function()
	local dap = require("dap")
	local dapui = require("dapui")

	require("dapui").setup()

	dap.listeners.before.attach.dapui_config = function()
		dapui.open()
	end
	dap.listeners.before.launch.dapui_config = function()
		dapui.open()
	end
	dap.listeners.before.event_terminated.dapui_config = function()
		dapui.close()
	end
	dap.listeners.before.event_exited.dapui_config = function()
		dapui.close()
	end

	vim.keymap.set("n", "<Leader>dt", dap.toggle_breakpoint, {})
	vim.keymap.set("n", "<Leader>dc", dap.continue, {})

	-- Section: <leader>d
	vim.keymap.set("n", "<F5>", dap.continue, {})
	vim.keymap.set("n", "<leader>de", dap.run_to_cursor, {})
	-- TODO: `dd` should start last debugging session (with recompilation) if no active session.
	vim.keymap.set("n", "<F10>", dap.step_over, {})
	vim.keymap.set("n", "<F8>", dap.step_into, {})
	vim.keymap.set("n", "<F7>", dap.step_out, {})
	vim.keymap.set("n", "<F9>", dap.toggle_breakpoint, {})
	vim.keymap.set("n", "<leader>dg", dap.step_out, {})
	vim.keymap.set("n", "<leader>dr", dap.restart, {})
	vim.keymap.set("n", "<leader>ds", dap.pause, {})
	vim.keymap.set("n", "<leader>dt", dap.terminate, {})
	vim.keymap.set("n", "<leader>du", dapui.toggle, {})
	vim.keymap.set("n", "de", dapui.eval, { silent = true })
	-- Set a keymap in normal mode for <leader>t to toggle terminal
	vim.keymap.set("n", "<leader>t", function()
		-- Initialize variable to hold terminal buffer number, if found
		local term_bufnr = nil

		-- Iterate over all open buffers
		for _, bufnr in ipairs(vim.api.nvim_list_bufs()) do
			-- Check if buffer type is 'terminal'
			if vim.api.nvim_buf_get_option(bufnr, "buftype") == "terminal" then
				term_bufnr = bufnr -- Save terminal buffer number
				break -- Exit loop once a terminal is found
			end
		end

		-- If a terminal buffer was found, close it
		if term_bufnr then
			vim.cmd("bd! " .. term_bufnr) -- Force close the terminal buffer
		else
			-- Otherwise, open a new terminal in a horizontal split
			vim.cmd("split | terminal")
		end
	end, { noremap = true, silent = true }) -- Keymap options: no remap and silent
	require("invictus.daps.jsts_dap")
	require("invictus.daps.python_dap")
	require("invictus.daps.cpp_dap")
	require("invictus.daps.lua_dap")
	require("netcoredbg-macOS-arm64").setup(require("dap"))
	--require("invictus.daps.dotnet_dap")
end

return M
