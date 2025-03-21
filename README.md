# Crafty Controller integration for Home Assistant
## Development
Add this to home assistant core devcontainers:

Remember to replace `$(pwd)` with this project absolute path
```json
{
  "mounts": [
    "source=$(pwd),target=/workspaces/ha-core/config/custom_components/crafty_controller,type=bind,consistency=cached"
  ]
}
```

Add `"--network=host"` to `runArgs`