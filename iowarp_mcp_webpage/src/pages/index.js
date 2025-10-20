import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import MCPShowcase from '@site/src/components/MCPShowcase';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Open-source MCP servers for Claude Code, Cursor, VS Code, Gemini. Connect AI to HDF5, ADIOS, Slurm, Pandas. Scientific computing tools.">
      <main className="landingPage">

        {/* Hero */}
        <section className="hero">
          <div className="hero__content">
            {/* Gnosis box at top */}
            <div className="hero__eyebrow">
              <img src="/iowarp-mcps/img/logos/grc-logo.png" alt="GRC" className="hero__eyebrowLogo" />
              Gnosis Research Center
              <img src="/iowarp-mcps/img/logos/iit-logo.png" alt="IIT" className="hero__eyebrowLogoLarge" />
            </div>

            {/* Logo + Brand name horizontal */}
            <div className="hero__branding">
              <img
                src="/iowarp-mcps/img/iowarp_logo.png"
                alt="IoWarp Logo"
                className="hero__logo"
              />
              <h1 className="hero__brand">
                <span className="hero__brandLine">IOWARP</span>
                <span className="hero__brandLine">MCPs</span>
              </h1>
            </div>

            {/* Title */}
            <h2 className="hero__title">
              Talk to Data, Devices, Apps<br/>
              Science Skill for Agents
            </h2>

            {/* Buttons */}
            <div className="hero__actions">
              <Link className="button button--primary hero__cta" to="/docs/intro">
                Install in Seconds
              </Link>
              <Link className="button button--outline hero__cta" to="#browse">
                Explore Servers
              </Link>
              <Link className="button button--ghost hero__cta" href="https://github.com/iowarp/iowarp-mcps" rel="noopener noreferrer">
                Star on GitHub
              </Link>
            </div>

            {/* Subtitle - 2 lines */}
            <p className="hero__subtitle">
              Model Context Protocol (MCP) servers for scientific computing and HPC research.<br/>
              Connect your AI Agents (<a href="https://www.claude.com/product/claude-code" target="_blank" rel="noopener">Claude Code</a>,{' '}
              <a href="https://cursor.com/" target="_blank" rel="noopener">Cursor</a>,{' '}
              <a href="https://code.visualstudio.com/" target="_blank" rel="noopener">VS Code</a>,{' '}
              <a href="https://github.com/google-gemini/gemini-cli" target="_blank" rel="noopener">Gemini CLI</a>,{' '}
              <a href="https://opencode.ai/" target="_blank" rel="noopener">OpenCode</a>) to Science Skills.
            </p>

            {/* Three category cards - Inside hero */}
            <div className="hero__highlights">
              <div className="hero__highlightCard">
                <h3>Data Formats</h3>
                <p>
                  Give your AI agents the ability to read and explore scientific file formats.
                  They can navigate{' '}
                  <a href="https://www.hdfgroup.org/solutions/hdf5/" target="_blank" rel="noopener"><strong>HDF5</strong></a> hierarchies, inspect{' '}
                  <a href="https://adios2.readthedocs.io/" target="_blank" rel="noopener"><strong>ADIOS</strong></a> simulation outputs, and process{' '}
                  <a href="https://parquet.apache.org/" target="_blank" rel="noopener"><strong>Parquet</strong></a> columnar data.
                  Your agents understand real research data, not just CSV files.
                </p>
              </div>

              <div className="hero__highlightCard">
                <h3>Data Analytics</h3>
                <p>
                  Turn AI agents into research support tools that accelerate discovery.
                  They can search{' '}
                  <a href="https://arxiv.org/" target="_blank" rel="noopener"><strong>ArXiv</strong></a> papers, analyze{' '}
                  <a href="https://pandas.pydata.org/" target="_blank" rel="noopener"><strong>Pandas</strong></a> tabular datasets, generate{' '}
                  <a href="https://matplotlib.org/" target="_blank" rel="noopener"><strong>Matplotlib</strong></a> visualizations, and compile citations.
                  Your agents handle the tedious parts of research.
                </p>
              </div>

              <div className="hero__highlightCard">
                <h3>HPC Resources</h3>
                <p>
                  Equip AI agents to operate HPC clusters and manage computational resources.
                  They can submit jobs to{' '}
                  <a href="https://slurm.schedmd.com/" target="_blank" rel="noopener"><strong>Slurm</strong></a>, load environment modules, monitor{' '}
                  <a href="https://www.mcs.anl.gov/research/projects/darshan/" target="_blank" rel="noopener"><strong>Darshan</strong></a> I/O performance, and orchestrate{' '}
                  <a href="https://github.com/grc-iit/jarvis-cd" target="_blank" rel="noopener"><strong>Jarvis</strong></a> workflows.
                  Your agents become cluster operators.
                </p>
              </div>
            </div>

            {/* Footer - Single line */}
            <div className="hero__footer">
              Open-Source Community Project supported in part by the{' '}
              <img src="/iowarp-mcps/img/logos/nsf-logo.png" alt="NSF" className="hero__nsfLogo" />
              <a href="https://new.nsf.gov/" className="hero__footerLink" target="_blank" rel="noopener noreferrer">
                National Science Foundation (NSF)
              </a>
            </div>
          </div>
        </section>

        {/* MCP Showcase */}
        <div id="browse">
          <MCPShowcase />
        </div>

      </main>
    </Layout>
  );
}
