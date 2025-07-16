from fastapi import HTTPException
from jarvis_cd.basic.pkg import Pipeline
from jarvis_cd.basic.jarvis_manager import JarvisManager
import os
import json

async def create_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().create(pipeline_id).build_env().save()
        return {"pipeline_id": pipeline_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create failed: {e}")

async def load_pipeline(pipeline_id: str = None) -> dict:
    try:
        pipeline = Pipeline().load(pipeline_id)
        return {"pipeline_id": pipeline_id, "status": "loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Load failed: {e}")

async def append_pkg(
    pipeline_id: str,
    pkg_type: str,
    pkg_id: str = None,
    do_configure: bool = True,
    **kwargs
) -> dict:
    try:
        # Avoid duplicate do_configure in kwargs
        raw_kwargs = dict(kwargs)
        config_flag = do_configure
        if 'do_configure' in raw_kwargs:
            config_flag = raw_kwargs.pop('do_configure')

        pipeline = Pipeline().load(pipeline_id)
        pipeline.append(
            pkg_type,
            pkg_id=pkg_id,
            do_configure=config_flag,
            **raw_kwargs
        ).save()
        return {"pipeline_id": pipeline_id, "appended": pkg_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Append failed: {e}")


async def build_pipeline_env(pipeline_id: str) -> dict:
    """
    Load a Jarvis-CD pipeline, rebuild its environment cache,
    tracking only CMAKE_PREFIX_PATH and PATH from the current shell, then save.
    """
    try:
        # 1. Load the existing pipeline
        pipeline = Pipeline().load(pipeline_id)

        # 2. Always track these two vars
        default_keys = ["CMAKE_PREFIX_PATH", "PATH"]
        env_track_dict = {key: True for key in default_keys}

        # 3. Rebuild the env cache, track only those vars, and save
        pipeline.build_env(env_track_dict).save()

        return {
            "pipeline_id": pipeline_id,
            "status": "environment_built"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Build env failed: {e}")


async def update_pipeline(pipeline_id: str) -> dict:
    """
    Re-apply the current environment & configuration to every pkg in the pipeline,
    then persist the updated pipeline.
    """
    try:
        pipeline = Pipeline().load(pipeline_id)
        pipeline.update()  # re-run configure on all sub-pkgs
        pipeline.save()    # persist any changes
        return {"pipeline_id": pipeline_id, "status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")


async def configure_pkg(pipeline_id: str, pkg_id: str, **kwargs) -> dict:
    try:
        pipeline = Pipeline().load(pipeline_id)
        # configure the pkg (this does NOT return self)
        pipeline.configure(pkg_id, **kwargs)

        # now save the entire pipeline (which will recurse and save each sub-pkg)
        pipeline.save()
        return {"pipeline_id": pipeline_id, "configured": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configure failed: {e}")

async def get_pkg_config(pipeline_id: str, pkg_id: str) -> dict:
    try:
        # 1. Load the pipeline
        pipeline = Pipeline().load(pipeline_id)

        # 2. Lookup the pkg
        pkg = pipeline.get_pkg(pkg_id)
        if pkg is None:
            raise HTTPException(status_code=404, detail=f"Package '{pkg_id}' not found")

        # 3. Return its config dict
        return {
            "pipeline_id": pipeline.global_id,
            "pkg_id": pkg_id,
            "config": pkg.config
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get config failed: {e}")

async def unlink_pkg(pipeline_id: str, pkg_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).unlink(pkg_id).save()
        return {"pipeline_id": pipeline_id, "unlinked": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unlink failed: {e}")

async def remove_pkg(pipeline_id: str, pkg_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).remove(pkg_id).save()
        return {"pipeline_id": pipeline_id, "removed": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Remove failed: {e}")

async def run_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).run()
        return {"pipeline_id": pipeline_id, "status": "running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Run failed: {e}")

async def destroy_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).destroy()
        return {"pipeline_id": pipeline_id, "status": "destroyed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Destroy failed: {e}")

async def get_all_packages() -> dict:
    """
    Get a comprehensive list of all available packages across all repositories.
    Returns package names, types, descriptions, capabilities, and configuration options.
    """
    try:
        manager = JarvisManager.get_instance()
        all_packages = {}
        
        # Get all repositories
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            
            if not os.path.exists(repo_path):
                continue
                
            # Look for packages in the repository
            packages_dir = os.path.join(repo_path, repo_name)
            if os.path.exists(packages_dir):
                for item in os.listdir(packages_dir):
                    pkg_path = os.path.join(packages_dir, item)
                    if os.path.isdir(pkg_path) and not item.startswith('_'):
                        # Try to get package information
                        pkg_file = os.path.join(pkg_path, 'pkg.py')
                        readme_file = os.path.join(pkg_path, 'README.md')
                        
                        description = "No description available"
                        capabilities = []
                        config_options = {}
                        
                        # Extract description from README first
                        if os.path.exists(readme_file):
                            try:
                                with open(readme_file, 'r') as f:
                                    lines = f.readlines()[:5]  # First 5 lines
                                    description = ' '.join([line.strip() for line in lines if line.strip()])[:300]
                            except:
                                pass
                        
                        # Extract capabilities and config from pkg.py
                        if os.path.exists(pkg_file):
                            try:
                                with open(pkg_file, 'r') as f:
                                    content = f.read()
                                    
                                    # Extract class docstring
                                    if description == "No description available":
                                        import re
                                        docstring_match = re.search(r'class.*?"""(.*?)"""', content, re.DOTALL)
                                        if docstring_match:
                                            description = docstring_match.group(1).strip()[:300]
                                    
                                    # Extract configuration menu items to understand capabilities
                                    if '_configure_menu' in content:
                                        # Try to extract menu configuration dynamically
                                        try:
                                            # Construct a temporary package to get config menu
                                            pkg_obj = manager.construct_pkg(item)
                                            if hasattr(pkg_obj, '_configure_menu'):
                                                menu_items = pkg_obj._configure_menu()
                                                for config in menu_items:
                                                    param_name = config.get('name', 'unknown')
                                                    param_type = config.get('type', 'str').__name__ if hasattr(config.get('type'), '__name__') else str(config.get('type', 'unknown'))
                                                    param_default = config.get('default', None)
                                                    param_choices = config.get('choices', [])
                                                    param_msg = config.get('msg', '')
                                                    
                                                    config_options[param_name] = {
                                                        'type': param_type,
                                                        'default': param_default,
                                                        'description': param_msg,
                                                        'choices': param_choices
                                                    }
                                        except Exception as e:
                                            # If we can't construct the package, skip capability extraction
                                            pass
                                    
                                    # Look for common capability patterns in the code
                                    capability_patterns = {
                                        'configurable_block_sizes': ['block_size', 'xfer', 'buffer_size'],
                                        'parallel_execution': ['nprocs', 'ppn', 'mpi'],
                                        'read_operations': ['read', 'input'],
                                        'write_operations': ['write', 'output'],
                                        'supports_hdf5': ['hdf5', 'h5'],
                                        'supports_mpiio': ['mpiio', 'mpi-io'],
                                        'supports_posix': ['posix'],
                                        'api_selection': ['api']
                                    }
                                    
                                    for capability, patterns in capability_patterns.items():
                                        if any(pattern in content.lower() for pattern in patterns):
                                            capabilities.append(capability)
                                            
                            except Exception as e:
                                # If we can't read the file, continue with empty capabilities
                                pass
                        
                        all_packages[item] = {
                            "name": item,
                            "repository": repo_name,
                            "description": description,
                            "path": pkg_path,
                            "available": os.path.exists(pkg_file),
                            "capabilities": capabilities,
                            "configuration_options": config_options,
                            "total_config_params": len(config_options)
                        }
        
        return {
            "status": "success",
            "total_packages": len(all_packages),
            "repositories_scanned": len(manager.repos),
            "packages": all_packages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get packages failed: {e}")


async def get_all_repos() -> dict:
    """
    Get a comprehensive list of all registered repositories.
    Returns repository names, paths, status, and package counts.
    """
    try:
        manager = JarvisManager.get_instance()
        all_repos = {}
        
        # Get all repositories
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            
            # Check if repository path exists
            path_exists = os.path.exists(repo_path)
            
            # Count packages in the repository
            package_count = 0
            packages_list = []
            
            if path_exists:
                # Look for packages in the repository
                packages_dir = os.path.join(repo_path, repo_name)
                if os.path.exists(packages_dir):
                    for item in os.listdir(packages_dir):
                        pkg_path = os.path.join(packages_dir, item)
                        if os.path.isdir(pkg_path) and not item.startswith('_'):
                            package_count += 1
                            packages_list.append(item)
            
            # Get repository metadata if available
            repo_info_file = os.path.join(repo_path, 'repo_info.json') if path_exists else None
            description = "No description available"
            version = "Unknown"
            maintainer = "Unknown"
            
            if repo_info_file and os.path.exists(repo_info_file):
                try:
                    with open(repo_info_file, 'r') as f:
                        repo_info = json.load(f)
                        description = repo_info.get('description', description)
                        version = repo_info.get('version', version)
                        maintainer = repo_info.get('maintainer', maintainer)
                except:
                    pass
            
            # Check for README in repository root
            readme_file = os.path.join(repo_path, 'README.md') if path_exists else None
            if readme_file and os.path.exists(readme_file) and description == "No description available":
                try:
                    with open(readme_file, 'r') as f:
                        lines = f.readlines()[:3]  # First 3 lines
                        description = ' '.join([line.strip() for line in lines if line.strip() and not line.startswith('#')])[:200]
                except:
                    pass
            
            all_repos[repo_name] = {
                "name": repo_name,
                "path": repo_path,
                "description": description,
                "version": version,
                "maintainer": maintainer,
                "path_exists": path_exists,
                "package_count": package_count,
                "packages": packages_list,
                "status": "active" if path_exists else "inactive"
            }
        
        return {
            "status": "success",
            "total_repositories": len(all_repos),
            "active_repositories": len([r for r in all_repos.values() if r["status"] == "active"]),
            "inactive_repositories": len([r for r in all_repos.values() if r["status"] == "inactive"]),
            "total_packages_across_repos": sum(r["package_count"] for r in all_repos.values()),
            "repositories": all_repos
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get repositories failed: {e}")


async def get_package_info(
    package_name: str,
    return_description: bool = True,
    return_readme: bool = True,
    return_configuration: bool = True,
    return_capabilities: bool = True,
    return_outputs: bool = False,
    return_installation: bool = False,
    return_usage_examples: bool = False
) -> dict:
    """
    Get detailed information about a specific package.
    
    Args:
        package_name: Name of the package to get information about
        return_description: Include package description
        return_readme: Include full README content
        return_configuration: Include configuration parameters
        return_capabilities: Include package capabilities
        return_outputs: Include information about outputs (extracted from README)
        return_installation: Include installation instructions (extracted from README)
        return_usage_examples: Include usage examples (extracted from README)
    
    Returns:
        Detailed package information based on requested components
    """
    try:
        manager = JarvisManager.get_instance()
        
        # Find the package across all repositories
        package_info = None
        package_path = None
        repository_name = None
        
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            
            if not os.path.exists(repo_path):
                continue
                
            # Look for the package in this repository
            packages_dir = os.path.join(repo_path, repo_name)
            if os.path.exists(packages_dir):
                pkg_path = os.path.join(packages_dir, package_name)
                if os.path.isdir(pkg_path):
                    package_path = pkg_path
                    repository_name = repo_name
                    break
        
        if not package_path:
            raise HTTPException(status_code=404, detail=f"Package '{package_name}' not found")
        
        # Initialize result structure
        result = {
            "package_name": package_name,
            "repository": repository_name,
            "path": package_path,
            "status": "success"
        }
        
        # Get basic package files
        pkg_file = os.path.join(package_path, 'pkg.py')
        readme_file = os.path.join(package_path, 'README.md')
        
        result["files_available"] = {
            "pkg_py": os.path.exists(pkg_file),
            "readme_md": os.path.exists(readme_file)
        }
        
        # Extract description
        if return_description:
            description = "No description available"
            
            # Try README first
            if os.path.exists(readme_file):
                try:
                    with open(readme_file, 'r') as f:
                        content = f.read()
                        lines = content.split('\n')
                        # Get first non-empty, non-header line
                        for line in lines[:10]:
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('```'):
                                description = line[:300]
                                break
                except:
                    pass
            
            # Fallback to pkg.py docstring
            if description == "No description available" and os.path.exists(pkg_file):
                try:
                    with open(pkg_file, 'r') as f:
                        content = f.read()
                        import re
                        docstring_match = re.search(r'class.*?"""(.*?)"""', content, re.DOTALL)
                        if docstring_match:
                            description = docstring_match.group(1).strip()[:300]
                except:
                    pass
            
            result["description"] = description
        
        # Extract full README content
        if return_readme:
            readme_content = "README not available"
            if os.path.exists(readme_file):
                try:
                    with open(readme_file, 'r') as f:
                        readme_content = f.read()
                except:
                    readme_content = "Error reading README file"
            result["readme_content"] = readme_content
        
        # Extract configuration parameters
        if return_configuration:
            config_options = {}
            if os.path.exists(pkg_file):
                try:
                    # Try to construct the package to get config menu
                    pkg_obj = manager.construct_pkg(package_name)
                    if hasattr(pkg_obj, '_configure_menu'):
                        menu_items = pkg_obj._configure_menu()
                        for config in menu_items:
                            param_name = config.get('name', 'unknown')
                            param_type = config.get('type', 'str').__name__ if hasattr(config.get('type'), '__name__') else str(config.get('type', 'unknown'))
                            param_default = config.get('default', None)
                            param_choices = config.get('choices', [])
                            param_msg = config.get('msg', '')
                            
                            config_options[param_name] = {
                                'type': param_type,
                                'default': param_default,
                                'description': param_msg,
                                'choices': param_choices
                            }
                except Exception as e:
                    config_options = {"error": f"Could not extract configuration: {e}"}
            
            result["configuration_parameters"] = config_options
            result["total_config_params"] = len(config_options) if isinstance(config_options, dict) and "error" not in config_options else 0
        
        # Extract capabilities
        if return_capabilities:
            capabilities = []
            if os.path.exists(pkg_file):
                try:
                    with open(pkg_file, 'r') as f:
                        content = f.read()
                        
                        # Look for common capability patterns in the code
                        capability_patterns = {
                            'configurable_block_sizes': ['block_size', 'xfer', 'buffer_size'],
                            'parallel_execution': ['nprocs', 'ppn', 'mpi'],
                            'read_operations': ['read', 'input'],
                            'write_operations': ['write', 'output'],
                            'supports_hdf5': ['hdf5', 'h5'],
                            'supports_mpiio': ['mpiio', 'mpi-io'],
                            'supports_posix': ['posix'],
                            'api_selection': ['api']
                        }
                        
                        for capability, patterns in capability_patterns.items():
                            if any(pattern in content.lower() for pattern in patterns):
                                capabilities.append(capability)
                except:
                    pass
            
            result["capabilities"] = capabilities
        
        # Extract outputs information from README
        if return_outputs and os.path.exists(readme_file):
            try:
                with open(readme_file, 'r') as f:
                    content = f.read()
                    
                    # Look for sections about outputs
                    output_info = []
                    lines = content.split('\n')
                    in_output_section = False
                    
                    for line in lines:
                        line_lower = line.lower()
                        if any(keyword in line_lower for keyword in ['output', 'result', 'generate', 'produce']):
                            if line.strip().startswith('#'):
                                in_output_section = True
                                output_info.append(line)
                            elif in_output_section and line.strip():
                                output_info.append(line)
                            elif in_output_section and not line.strip():
                                in_output_section = False
                    
                    result["outputs_info"] = '\n'.join(output_info) if output_info else "No output information found in README"
            except:
                result["outputs_info"] = "Error extracting output information"
        
        # Extract installation instructions
        if return_installation and os.path.exists(readme_file):
            try:
                with open(readme_file, 'r') as f:
                    content = f.read()
                    
                    # Look for installation sections
                    install_info = []
                    lines = content.split('\n')
                    in_install_section = False
                    
                    for line in lines:
                        line_lower = line.lower()
                        if 'installation' in line_lower or 'install' in line_lower:
                            if line.strip().startswith('#'):
                                in_install_section = True
                                install_info.append(line)
                            elif in_install_section:
                                install_info.append(line)
                        elif in_install_section and line.strip().startswith('#'):
                            # New section started
                            break
                    
                    result["installation_info"] = '\n'.join(install_info) if install_info else "No installation information found in README"
            except:
                result["installation_info"] = "Error extracting installation information"
        
        # Extract usage examples
        if return_usage_examples and os.path.exists(readme_file):
            try:
                with open(readme_file, 'r') as f:
                    content = f.read()
                    
                    # Look for usage/example sections and code blocks
                    usage_info = []
                    lines = content.split('\n')
                    in_usage_section = False
                    in_code_block = False
                    
                    for line in lines:
                        line_lower = line.lower()
                        
                        # Check for usage/example headers
                        if any(keyword in line_lower for keyword in ['usage', 'example', 'run', 'experiment']):
                            if line.strip().startswith('#'):
                                in_usage_section = True
                                usage_info.append(line)
                                continue
                        
                        # Handle code blocks
                        if line.strip().startswith('```'):
                            in_code_block = not in_code_block
                            if in_usage_section:
                                usage_info.append(line)
                            continue
                        
                        # Add content if in usage section
                        if in_usage_section:
                            usage_info.append(line)
                            # Stop at next major section
                            if line.strip().startswith('#') and not any(keyword in line_lower for keyword in ['usage', 'example', 'run', 'experiment']):
                                break
                    
                    result["usage_examples"] = '\n'.join(usage_info) if usage_info else "No usage examples found in README"
            except:
                result["usage_examples"] = "Error extracting usage examples"
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get package info failed: {e}")