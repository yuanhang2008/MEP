# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note: CHANGELOG was created in version 1.1.0, so change logs in versions that prior to 1.1.0 may be imprecise, if some of logs are wrong, please file an issue.

## [unreleased]

## [1.2.0] - 2025-7-25

### Added

- Add Safe Mode(It is enabled by default and cannot be changed dynamically) in config.
- Add "Math.mathfunc" to get a math function by name.
- Add "Numeric" class to express a constant value in formula.
- "Expression" can be instantiated by user.

### Changed

- Rename function "Math.int" to "Math.toint", "Math.float" to "Math.tofloat", etc.
- Change the data structure of the expression tree.
- Optimize the check of tree type.
- Support symbol names consisting of letters + numbers.

### Removed

- Removed "symbols".

### Fixed

Math function can produce productions correctly.

## [1.1.4] - 2025-7-18

### Added

- Add requirement.txt.
- Add "README-cn.md" in Chinese.

### Changed

- Rename function "get" to "find".

### Fixed

- Ignore ".vscode" folder.

### Removed

- Remove "auto_install_1.bat" && "auto_install_2.bat". MEP needs to be installed manually now.
- Remove "draw" feature, but "draw.py" is kept.

## [1.1.3] - 2023-10-3

### Added

- Add config.py.

### Changed

- Rename COLOR to DEFULT_COLORS.
- Merge expressions by operators(unfinished).

### Fixed

- "_cache" attribute in Expression controls the maximum length.

### Removed

- Remove the using of draw(because there is soething unavoidable bugs, but code is kept).

## [1.1.2] - 2023-9-29

### Added

- Document strings.

### Changed

- Add newfunc and its subfunctions to the class Constructor.

## [1.1.1] - 2023-9-28

### Added

- Change log.
- Support to merge formulas by functions in Math.

### Changed

- Change math function "conditions" name to "branch".
- Change functions name "call_with_name" and "get_formula" to "call" and "get".

## [1.1.0] - 2023-9-16

### Added

- Merge formulas by operators.

### Changed

- Rewrite Draw.
- Beautify README.

## Removed

- Remove ```setmax``` in ```Draw```. 

### Fixed

- Labels show ```formula.text()``` now instead ```__str__()```.

## [1.0.3] - 2023-8-29

### Added

- Formula name.
- Function ```call_with_name``` and ```get_formula```.

## [1.0.2] - 2023-7-26

### Added

- Document strings(unfinished).
- Support comparison operator(unfinished, need r-mode).

## [1.0.1] - 2023-7-26

### Changed

- Better class delivering.

## [1.0.0] - 2023-7-24

### Added

- Class ```Helper``` in ```math.py```.
- Test files(unfinished).

### Changed

- Better granularity of methods.

## [0.8.3] - 2023-7-22

### Changed

- Show the GUI when using ```auto_install_1.bat```.

## [0.8.2] - 2023-7-22

### Changed

- Isolated methods ```text``` and ```__str__```.
- Args list is sorted.

## [0.8.1] - 2023-7-22

### Added

- More math functions.
- Draw precision.

### Changed

- Rewrite some parts of ```Draw```.

## [0.8.0] - 2023-7-21

### Added

- More math functions.

### Changed

- Support complex number.

## [0.7.0] - 2023-7-19

### Changed

- Develop mode to ```auto_install.bat```.

## [0.6.2] - 2023-7-18

### Added

- The closure function ```newfunc``` can produce math functions easily.

### Fixed

- ```Formula``` can identify a number as a production.

## [0.6.1] - 2023-7-18

### Changed

- ```Production``` is not accessible(maybe it was implemented in earlier versions).

### Fixed

- ```relock``` can avoid a production being accessed by users.

## [0.6.0] - 2023-7-18

### Added

- Formulas currying.
- Math function: ```sqrt```.

## [0.5.2] - 2023-7-17

### Added

- README: the math functions part.

### Changed

- README: rewrite the draw part.
- Better arguments delivering in some methods.

## [0.5.1] - 2023-7-17

### Changed

- A symbol can only consist of a single letter.
- In expressino trees, a symbol is stored as "$" + symbol name.

### Fixed

- Any strings are identified to a symbol.

## [0.5.0] - 2023-7-17

### Added

- File ```math.py```.
- Math Functions(unfinished).

### Changed

- Support parsing a function to tree.

### Fixed

- Identify any symbols instead of only "x" in method ```_get_exp```, ```Formula```, ```formula.py```.

## [0.4.1] - 2023-7-17

### Changed

- Rewrite ```auto_install.bat```.

## [0.4.0] - 2023-7-17

### Added

- Class ```Symbol```.

## [0.3.0] - 2023-7-16

### Added

- README: the draw formula part.

### Changed

- Remove meaningless parentheses in expression texts.
- Improve ```Drawer```.

## [0.2.0] - 2023-7-15

The first version of MEP released (Versions prior to 0.2.0 are deprecated).

### Added

- ```auto_install.bat``` instead pip.
- Class ```Formula``` and ```Expression```.

[unreleased]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.2.0...HEAD
[1.2.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.1.4...MEP-v1.2.0
[1.1.4]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.1.3...MEP-v1.1.4
[1.1.3]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.1.2...MEP-v1.1.3
[1.1.2]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.1.1...MEP-v1.1.2
[1.1.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.1.0...MEP-v1.1.1
[1.1.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.0.3...MEP-v1.1.0
[1.0.3]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.0.2...MEP-v1.0.3
[1.0.2]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.0.1...MEP-v1.0.2
[1.0.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v1.0.0...MEP-v1.0.1
[1.0.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.8.3...MEP-v1.0.0
[0.8.3]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.8.2...MEP-v0.8.3
[0.8.2]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.8.1...MEP-v0.8.2
[0.8.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.8.0...MEP-v0.8.1
[0.8.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.7.0...MEP-v0.8.0
[0.7.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.6.2...MEP-v0.7.0
[0.6.2]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.6.1...MEP-v0.6.2
[0.6.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.6.0...MEP-v0.6.1
[0.6.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.5.2...MEP-v0.6.0
[0.5.2]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.5.1...MEP-v0.5.2
[0.5.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.5.0...MEP-v0.5.1
[0.5.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.4.1...MEP-v0.5.0
[0.4.1]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.4.0...MEP-v0.4.1
[0.4.0]: https://github.com/yuanhang2008/MEP/compare/MEP-v0.3.0...MEP-v0.4.0
[0.3.0]: https://github.com/yuanhang2008/MEP/compare/MEP...MEP-v0.3.0
[0.2.0]: https://github.com/yuanhang2008/MEP/releases/tag/MEP