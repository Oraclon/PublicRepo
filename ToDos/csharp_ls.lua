require("mason-lspconfig").setup({
  ensure_installed = {
    "clangd",
    "lua_ls",
    "csharp_ls", -- 👈 Add this
  },
})

["csharp_ls"] = function()
  require("lspconfig").csharp_ls.setup({
    on_attach = on_attach,
    capabilities = capabilities,
    -- Optional: add settings if needed
    settings = {
      csharp = {
        -- These settings depend on your needs; they can be left out for now
      }
    },
  })
end,
