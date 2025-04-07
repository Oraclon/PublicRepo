-- ~/.config/nvim/lua/plugins/init.lua
-- ...

{
    "williamboman/mason.nvim",
    opts = {
      ensure_installed = {
        "lua-language-server",
        "csharp-language-server",
      "omnisharp",
        "xmlformatter",
        "stylua",
        "bicep-lsp",
        "html-lsp",
        "css-lsp",
        "csharpier",
        "prettier",
        "json-lsp"
      },
    },
  },

  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      -- ensure_installed = "all"
      ensure_installed = {
        "vim",
        "lua",
        "vimdoc",
        "html",
        "css",
        "c_sharp",
        "bicep"
      },
    },
  },
