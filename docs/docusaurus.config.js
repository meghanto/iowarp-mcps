// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'IOWarp MCPs',
  tagline: 'Model Context Protocol servers for scientific computing research',
  favicon: 'img/iowarp_logo.png',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://iowarp.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/iowarp-mcps/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'iowarp', // Usually your GitHub org/user name.
  projectName: 'iowarp-mcps', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Enhanced metadata for social sharing
  metadata: [
    {name: 'description', content: 'Collection of Model Context Protocol (MCP) servers for scientific computing research. Enable AI agents to interact with data analysis tools, HPC resources, and research datasets.'},
    {name: 'keywords', content: 'MCP, Model Context Protocol, scientific computing, AI agents, data analysis, HPC, research, IOWarp'},
    {property: 'og:type', content: 'website'},
    {property: 'og:title', content: 'IOWarp MCPs - Scientific Computing Tools for AI'},
    {property: 'og:description', content: 'Collection of Model Context Protocol servers for scientific computing research. Enable AI agents to interact with data analysis tools, HPC resources, and research datasets.'},
    {property: 'og:image', content: 'https://iowarp.github.io/iowarp-mcps/img/iowarp_logo.png'},
    {property: 'twitter:card', content: 'summary_large_image'},
    {property: 'twitter:title', content: 'IOWarp MCPs - Scientific Computing Tools for AI'},
    {property: 'twitter:description', content: 'Collection of Model Context Protocol servers for scientific computing research.'},
    {property: 'twitter:image', content: 'https://iowarp.github.io/iowarp-mcps/img/iowarp_logo.png'},
  ],

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: false,
          routeBasePath: 'docs',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/iowarp/iowarp-mcps/tree/main/docs/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card for link previews
      image: 'img/iowarp_logo.png',
      navbar: {
        title: 'IOWarp MCPs',
        logo: {
          alt: 'IOWarp MCPs Logo',
          src: 'img/iowarp_logo.png',
        },
        items: [
          {
            to: '/',
            position: 'left',
            label: 'Browse MCPs',
          },
          {
            to: '/docs/intro',
            position: 'left',
            label: 'Getting Started',
          },
          {
            href: 'https://github.com/iowarp/iowarp-mcps',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'MCPs',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/intro',
              },
              {
                label: 'All MCPs',
                to: '/docs/mcps/adios',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Issues',
                href: 'https://github.com/iowarp/iowarp-mcps/issues',
              },
              {
                label: 'Discussions',
                href: 'https://github.com/iowarp/iowarp-mcps/discussions',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/iowarp/iowarp-mcps',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} IOWarp. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
    }),
};

export default config;
