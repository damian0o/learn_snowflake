import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

// Overlay for Quartz 4 (https://quartz.jzhao.xyz/configuration).
// The Pages workflow clones Quartz at a pinned tag, copies this file over its
// default config, stages vault/ as content with tools/stage_site.py and builds.
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Learn Snowflake",
    pageTitleSuffix: " · Learn Snowflake",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    baseUrl: "damian0o.github.io/learn_snowflake",
    ignorePatterns: ["Templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#fafbfd",
          lightgray: "#e4e8ee",
          gray: "#aeb6c2",
          darkgray: "#4a5261",
          dark: "#1f2733",
          secondary: "#1f6fb2",
          tertiary: "#29b5e8",
          highlight: "rgba(41, 181, 232, 0.12)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#14181f",
          lightgray: "#2b323d",
          gray: "#5d6673",
          darkgray: "#cfd6e0",
          dark: "#eef2f7",
          secondary: "#6fb6ff",
          tertiary: "#29b5e8",
          highlight: "rgba(41, 181, 232, 0.14)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      // Content is staged out of the git tree, so no git dates.
      Plugin.CreatedModifiedDate({ priority: ["frontmatter", "filesystem"] }),
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: false }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
