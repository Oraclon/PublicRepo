require("mason-lspconfig").setup({
  ensure_installed = {
    "pyright",  -- Add Python LSP (Pyright)
    "clangd",
    "lua_ls",
    "csharp_ls",
    "tsserver",
  },
})

-- Add to your setup_handlers() or part of default LSP config
require("mason-lspconfig").setup_handlers({
  -- Default handler for all LSPs
  function(server_name)
    require("lspconfig")[server_name].setup({
      on_attach = on_attach,
      capabilities = capabilities,
    })
  end,

  -- Custom handler for pyright (Python)
  ["pyright"] = function()
    require("lspconfig").pyright.setup({
      on_attach = on_attach,
      capabilities = capabilities,
      settings = {
        python = {
          analysis = {
            autoSearchPaths = true,
            useLibraryCodeForTypes = true,
            diagnosticMode = "openFilesOnly",  -- Controls the scope of diagnostics
          },
        },
      },
    })
  end,
})
