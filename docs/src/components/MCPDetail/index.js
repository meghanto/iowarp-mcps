import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CodeBlock from '@theme/CodeBlock';
import styles from './styles.module.css';

const MCPDetail = ({ 
  name, 
  icon, 
  category, 
  description, 
  version, 
  actions, 
  platforms,
  children 
}) => {
  const [activeInstallTab, setActiveInstallTab] = useState('cursor');

  const installationConfigs = {
    cursor: {
      title: 'Cursor',
      language: 'json',
      code: `{
  "mcpServers": {
    "${name.toLowerCase()}-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "${name.toLowerCase()}"]
    }
  }
}`
    },
    vscode: {
      title: 'VS Code',
      language: 'json',
      code: `"mcp": {
  "servers": {
    "${name.toLowerCase()}-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "${name.toLowerCase()}"]
    }
  }
}`
    },
    claude_code: {
      title: 'Claude Code',
      language: 'bash',
      code: `claude mcp add ${name.toLowerCase()}-mcp -- uvx iowarp-mcps ${name.toLowerCase()}`
    },
    claude_desktop: {
      title: 'Claude Desktop',
      language: 'json',
      code: `{
  "mcpServers": {
    "${name.toLowerCase()}-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "${name.toLowerCase()}"]
    }
  }
}`
    },
    manual: {
      title: 'Manual Setup',
      language: 'bash',
      code: `# Linux/macOS
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/${name} run ${name.toLowerCase()}-mcp --help

# Windows CMD
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\\iowarp-mcps\\mcps\\${name} run ${name.toLowerCase()}-mcp --help

# Windows PowerShell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\\iowarp-mcps\\mcps\\${name} run ${name.toLowerCase()}-mcp --help`
    }
  };

  const getPlatformIcon = (platform) => {
    const icons = {
      claude: '🤖',
      cursor: '⚡',
      vscode: '💻'
    };
    return icons[platform] || '🔧';
  };

  return (
    <div className={styles.mcpDetail}>
      {/* Header */}
      <div className={styles.header}>
        <Link to="/" className={styles.backButton}>
          ← Back to MCPs
        </Link>
        
        <div className={styles.mcpInfo}>
          <div className={styles.mcpHeader}>
            <div className={styles.mcpIcon}>{icon}</div>
            <div className={styles.mcpTitleSection}>
              <h1 className={styles.mcpTitle}>{name}</h1>
              <div className={styles.mcpMeta}>
                <span className={styles.mcpCategory}>{category}</span>
                <span className={styles.mcpVersion}>v{version}</span>
                <div className={styles.platformSupport}>
                  {platforms.map(platform => (
                    <span key={platform} className={styles.platformIcon} title={platform}>
                      {getPlatformIcon(platform)}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
          <p className={styles.mcpDescription}>{description}</p>
        </div>
      </div>

      {/* Quick Installation */}
      <div className={styles.quickInstall}>
        <h2 className={styles.sectionTitle}>🚀 Quick Installation</h2>
        
        <div className={styles.installTabs}>
          {Object.entries(installationConfigs).map(([key, config]) => (
            <button
              key={key}
              className={`${styles.installTab} ${activeInstallTab === key ? styles.active : ''}`}
              onClick={() => setActiveInstallTab(key)}
            >
              {config.title}
            </button>
          ))}
        </div>

        <div className={styles.installContent}>
          <CodeBlock language={installationConfigs[activeInstallTab].language}>
            {installationConfigs[activeInstallTab].code}
          </CodeBlock>
        </div>
      </div>

      {/* Actions Overview */}
      {actions && actions.length > 0 && (
        <div className={styles.actionsSection}>
          <h2 className={styles.sectionTitle}>🔧 Available Actions</h2>
          <div className={styles.actionsGrid}>
            {actions.map((action, index) => (
              <div key={index} className={styles.actionCard}>
                <code className={styles.actionName}>{action}</code>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Additional content from markdown */}
      <div className={styles.detailContent}>
        {children}
      </div>

      {/* Footer */}
      <div className={styles.footer}>
        <div className={styles.footerLinks}>
          <Link href="https://github.com/iowarp/iowarp-mcps" className={styles.footerLink}>
            📖 View on GitHub
          </Link>
          <Link href="https://github.com/iowarp/iowarp-mcps/issues" className={styles.footerLink}>
            🐛 Report Issue
          </Link>
        </div>
        <p className={styles.footerText}>
          Part of the IoWarp MCPs collection - bringing AI practically to science!
        </p>
      </div>
    </div>
  );
};

export default MCPDetail;