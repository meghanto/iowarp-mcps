import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import CodeBlock from '@theme/CodeBlock';
import MDXContent from '@theme/MDXContent';
import styles from './styles.module.css';

const MCPDetail = ({ 
  name, 
  icon, 
  category, 
  description, 
  version, 
  actions, 
  platforms,
  keywords,
  license,
  tools = [],
  children 
}) => {
  const [activeTab, setActiveTab] = useState('installation');
  const [activeInstallTab, setActiveInstallTab] = useState('cursor');
  const [expandedAction, setExpandedAction] = useState(null);

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

  // For now, we'll render all children content in the examples tab
  // The markdown is now structured to only contain examples
  const renderContent = (children) => {
    return children;
  };

  // Simple markdown-like renderer for tool descriptions
  const renderMarkdownDescription = (text) => {
    if (!text) return <p>No description available.</p>;
    
    // Split by bullet points and render as list
    const lines = text.split('\n').filter(line => line.trim());
    const hasBullets = lines.some(line => line.trim().startsWith('-') || line.trim().startsWith('*'));
    
    if (hasBullets) {
      const listItems = lines
        .filter(line => line.trim().startsWith('-') || line.trim().startsWith('*'))
        .map((line, index) => (
          <li key={index}>{line.replace(/^[\s\-\*]+/, '').trim()}</li>
        ));
      
      const nonListContent = lines
        .filter(line => !(line.trim().startsWith('-') || line.trim().startsWith('*')))
        .join(' ');
      
      return (
        <div>
          {nonListContent && <p>{nonListContent}</p>}
          {listItems.length > 0 && <ul>{listItems}</ul>}
        </div>
      );
    }
    
    return <p>{text}</p>;
  };

  const toggleAction = (actionName) => {
    setExpandedAction(expandedAction === actionName ? null : actionName);
  };

  // Generate TOC based on active tab
  const generateTOC = () => {
    const tocItems = [];
    
    if (activeTab === 'installation') {
      tocItems.push(
        { id: 'installation', title: 'Installation', level: 2 },
        ...Object.keys(installationConfigs).map(key => ({
          id: `install-${key}`,
          title: installationConfigs[key].title,
          level: 3
        }))
      );
    } else if (activeTab === 'actions' && tools && tools.length > 0) {
      tocItems.push(
        { id: 'actions', title: 'Actions', level: 2 },
        ...tools.map(tool => ({
          id: `action-${tool.name}`,
          title: tool.name,
          level: 3
        }))
      );
    } else if (activeTab === 'examples') {
      tocItems.push({ id: 'examples', title: 'Examples', level: 2 });
      // Extract headings from children content if they exist
      if (children && typeof children === 'string') {
        const headingMatches = children.match(/^###?\s+(.+)$/gm);
        if (headingMatches) {
          headingMatches.forEach((heading, index) => {
            const level = heading.startsWith('###') ? 3 : 2;
            const title = heading.replace(/^###?\s+/, '');
            tocItems.push({
              id: `example-${index}`,
              title: title,
              level: level
            });
          });
        }
      }
    }
    
    return tocItems;
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
          
          {/* Project Information */}
          {(keywords || license) && (
            <div className={styles.projectInfo}>
              {keywords && keywords.length > 0 && (
                <div className={styles.projectInfoItem}>
                  <strong>Keywords:</strong> {keywords.slice(0, 8).join(', ')}
                </div>
              )}
              {license && (
                <div className={styles.projectInfoItem}>
                  <strong>License:</strong> {license}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Tab Navigation */}
      <div className={styles.tabNavigation}>
        <button 
          className={`${styles.mainTab} ${activeTab === 'installation' ? styles.active : ''}`}
          onClick={() => setActiveTab('installation')}
        >
          📥 Installation
        </button>
        <button 
          className={`${styles.mainTab} ${activeTab === 'actions' ? styles.active : ''}`}
          onClick={() => setActiveTab('actions')}
        >
          🔧 Actions ({actions?.length || 0})
        </button>
        <button 
          className={`${styles.mainTab} ${activeTab === 'examples' ? styles.active : ''}`}
          onClick={() => setActiveTab('examples')}
        >
          📝 Examples
        </button>
      </div>

      {/* Main Layout with TOC */}
      <div className={styles.mainLayout}>
        {/* Tab Content */}
        <div className={styles.tabContent}>
        {activeTab === 'installation' && (
          <div className={styles.installationTab}>
            <div className={styles.quickInstall}>
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
          </div>
        )}

        {activeTab === 'actions' && (
          <div className={styles.actionsTab}>
            {tools && tools.length > 0 ? (
              <div className={styles.actionsGrid}>
                {tools.map((tool, index) => (
                  <div key={index} className={`${styles.actionCard} ${expandedAction === tool.name ? styles.expanded : ''}`} onClick={() => toggleAction(tool.name)}>
                    <div className={styles.actionHeader}>
                      <code className={styles.actionName}>{tool.name}</code>
                      <span className={styles.actionToggle}>
                        {expandedAction === tool.name ? '▼' : '▶'}
                      </span>
                    </div>
                    {expandedAction === tool.name && (
                      <div className={styles.actionDescription}>
                        {renderMarkdownDescription(tool.description)}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : actions && actions.length > 0 && (
              <div className={styles.actionsGrid}>
                {actions.map((action, index) => (
                  <div key={index} className={`${styles.actionCard} ${expandedAction === action ? styles.expanded : ''}`} onClick={() => toggleAction(action)}>
                    <div className={styles.actionHeader}>
                      <code className={styles.actionName}>{action}</code>
                      <span className={styles.actionToggle}>
                        {expandedAction === action ? '▼' : '▶'}
                      </span>
                    </div>
                    {expandedAction === action && (
                      <div className={styles.actionDescription}>
                        <p>Tool functionality: {action.replace('_', ' ').toLowerCase()}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'examples' && (
          <div className={styles.examplesTab}>
            <div className={styles.markdownContent}>
              {renderContent(children)}
            </div>
          </div>
        )}
        </div>

        {/* Table of Contents */}
        <div className={styles.tocSidebar}>
          <div className={styles.tocContent}>
            <h3 className={styles.tocTitle}>Contents</h3>
            <ul className={styles.tocList}>
              {generateTOC().map((item, index) => (
                <li key={index} className={`${styles.tocItem} ${styles[`tocLevel${item.level}`]}`}>
                  <a href={`#${item.id}`} className={styles.tocLink}>
                    {item.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
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
          Part of the IOWarp MCPs collection - bringing AI practically to science!
        </p>
      </div>
    </div>
  );
};

export default MCPDetail;