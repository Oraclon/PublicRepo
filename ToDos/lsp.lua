-- LSP Setup: mason + mason-lspconfig + lspconfig
local mason = require("mason")
local mason_lspconfig = require("mason-lspconfig")
local lspconfig = require("lspconfig")

-- LSP completion capabilities
local capabilities = require("cmp_nvim_lsp").default_capabilities()

-- Function to attach LSP keymaps
local function on_attach(_, bufnr)
  local nmap = function(keys, func, desc)
    vim.keymap.set("n", keys, func, { buffer = bufnr, desc = desc })
  end

  nmap("gd", vim.lsp.buf.definition, "Go to Definition")
  nmap("K", vim.lsp.buf.hover, "Hover")
  nmap("gi", vim.lsp.buf.implementation, "Go to Implementation")
  nmap("<leader>rn", vim.lsp.buf.rename, "Rename Symbol")
  nmap("<leader>ca", vim.lsp.buf.code_action, "Code Action")
  nmap("gr", vim.lsp.buf.references, "References")
  nmap("<leader>f", function() vim.lsp.buf.format({ async = true }) end, "Format Code")
end

-- Setup Mason
mason.setup()
mason_lspconfig.setup({
  ensure_installed = {
    "clangd",
    "lua_ls",
    "csharp_ls",
    "jsonls",
    "bashls",
    "tsserver",
  },
})

-- Setup all servers with optional overrides
mason_lspconfig.setup_handlers({
  -- Default setup
  function(server_name)
    lspconfig[server_name].setup({
      on_attach = on_attach,
      capabilities = capabilities,
    })
  end,

  -- Custom setup for clangd
  ["clangd"] = function()
    lspconfig.clangd.setup({
      cmd = { "clangd", "--background-index", "--clang-tidy" },
      on_attach = on_attach,
      capabilities = capabilities,
    })
  end,

  -- Custom setup for lua
  ["lua_ls"] = function()
    lspconfig.lua_ls.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        Lua = {
          diagnostics = {
            globals = { "vim" },
          },
          workspace = {
            checkThirdParty = false,
            library = vim.api.nvim_get_runtime_file("", true),
          },
        },
      },
    })
  end,
})
