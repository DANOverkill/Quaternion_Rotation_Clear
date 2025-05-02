# Blender Armature Rotation Converter Addon

A simple Blender addon that converts quaternion rotations to Euler XYZ and cleans up related animation keyframes.

## Features

- Converts all quaternion rotation modes to Euler XYZ for selected armatures
- Removes rotation mode keyframes automatically
- Reports remaining quaternion animation channels in the Info panel
- Adds convenient menu to the top bar
- Undo support

## Installation

1. Download the ziped file file. The is no need to unzip
2. In Blender, go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the downloaded ziped file
4. Enable the addon by checking the checkbox

## Usage

1. Select an armature object
2. In the top bar menu, go to `Scripts > Convert Quaternion to Euler`
3. Check the Info panel (top-left corner) for conversion results

**Note:** Only works with active armature objects with animation data.

## Compatibility

Tested with Blender 3.0+  
Should work with Blender 2.80 and newer

## License

[MIT License](LICENSE) - Feel free to modify and redistribute

## Troubleshooting

- Ensure you have an armature selected
- Make sure the armature has animation data
- Check the Info panel for conversion reports
- Report issues with error messages and reproduction steps

## Contributing

Contributions welcome! Please open an issue first to discuss proposed changes.

---

**Important:** After conversion, verify your animations as this process cannot be automatically reversed (use Blender's undo if needed).
