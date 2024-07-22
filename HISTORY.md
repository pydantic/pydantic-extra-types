# CHANGELOG

## Latest Changes

## 2.9.0

### Types

* Add Semantic version type. PR [#195](https://github.com/pydantic/pydantic-extra-types/pull/195) by [@nikstuckenbrock](https://github.com/nikstuckenbrock)
* Add timezone name validation. PR [#193](https://github.com/pydantic/pydantic-extra-types/pull/193) by [@07pepa](https://github.com/07pepa)

### Refactor

* Replace try-except block by if-else statement. PR [#192](https://github.com/pydantic/pydantic-extra-types/pull/192) by [@maxsos](https://github.com/maxsos)

### Dependencies

* ⬆ Bump the python-packages group with 4 updates.  PR [#194](https://github.com/pydantic/pydantic-extra-types/pull/194) by @dependabot

## 2.8.2

* 🐛 Preserve timezone information when validating Pendulum DateTimes. [#189](https://github.com/pydantic/pydantic-extra-types/pull/189) by [@chrisguidry
](https://github.com/chrisguidry)

## 2.8.1

### Bug Fixes

* 🐛 Fix Pendulum date time object to have correct typing. [#184](https://github.com/pydantic/pydantic-extra-types/pull/184) by [@07pepa](https://github.com/07pepa)

### Types

* ✨ Add parsing of pendulum_dt from unix time and non-strict parsing. [#185](https://github.com/pydantic/pydantic-extra-types/pull/185) by [@07pepa](https://github.com/07pepa)

## 2.8.0

### Refactor

* ♻️ refactor some functions & minor changes. [#180](https://github.com/pydantic/pydantic-extra-types/pull/180) by [@yezz123](https://github.com/yezz123)

### Internal

* Allow requiring extra dependencies. [#178](https://github.com/pydantic/pydantic-extra-types/pull/178) by [@yezz123](https://github.com/yezz123)

### Types

* Add ISO 15924 and tests. [#174](https://github.com/pydantic/pydantic-extra-types/pull/174) by [@07pepa](https://github.com/07pepa)
* add native datetime to pendulum_dt.py. [#176](https://github.com/pydantic/pydantic-extra-types/pull/176) by [@07pepa](https://github.com/07pepa)
* add hash and eq to phone_numbers. [#177](https://github.com/pydantic/pydantic-extra-types/pull/177) by [@07pepa](https://github.com/07pepa)

### Dependencies

* ⬆ Bump the python-packages group with 5 updates. PR [#179](https://github.com/pydantic/pydantic-extra-types/pull/179) by @dependabot
* ⬆ Bump the python-packages group with 4 updates. PR [#171](https://github.com/pydantic/pydantic-extra-types/pull/171) by @dependabot

## 2.7.0

* 🔥 Remove latest-changes workflow. PR [#165](https://github.com/pydantic/pydantic-extra-types/pull/165) by [yezz123](https://github.com/yezz123)
* 🔨 Add latest-changes workflow to generate Changes. PR [#164](https://github.com/pydantic/pydantic-extra-types/pull/164) by [yezz123](https://github.com/yezz123)
* Added LanguageAlpha2 and LanguageName types. PR [#153](https://github.com/pydantic/pydantic-extra-types/pull/153) by [odelmarcelle](https://github.com/odelmarcelle)
* Added support for pendulum Dates. PR [#154](https://github.com/pydantic/pydantic-extra-types/pull/154) by [Woody1193](https://github.com/Woody1193)
* Add support for pendulum Duration. PR [#162](https://github.com/pydantic/pydantic-extra-types/pull/162) by [tempookian](https://github.com/tempookian)

### Dependencies

* ⬆ Bump the python-packages group with 1 update. PR [#150](https://github.com/pydantic/pydantic-extra-types/pull/150) by [dependabot](https://github.com/dependabot)
* ⬆ Bump the python-packages group with 6 updates. PR [#160](https://github.com/pydantic/pydantic-extra-types/pull/160) by [dependabot](https://github.com/dependabot)

## 2.6.0

* Allow python-ulid 2.x on Python 3.9 and later. PR [#131](https://github.com/pydantic/pydantic-extra-types/pull/131) by [@musicinmybrain](https://github.com/musicinmybrain)
* Do not pin the ”major” version of pycountry. PR [#132](https://github.com/pydantic/pydantic-extra-types/pull/132) by [@musicinmybrain](https://github.com/musicinmybrain)
* 🤖 Create dependabot.yml for updating GitHub action. PR [#134](https://github.com/pydantic/pydantic-extra-types/pull/134) by [@yezz123](https://github.com/yezz123)
* Refactor Documentation for ISBN and MAC address modules. PR [#124](https://github.com/pydantic/pydantic-extra-types/pull/124) by [@yezz123](https://github.com/yezz123)
* Add language code definitions and test. PR [#141](https://github.com/pydantic/pydantic-extra-types/pull/141) by [@07pepa](https://github.com/07pepa)
* Create a `changelog` to match release notes. PR [#142](https://github.com/pydantic/pydantic-extra-types/pull/142) by [@yezz123](https://github.com/yezz123)
* Add currency code ISO 4217 and its subset that includes only currencies. PR [#143](https://github.com/pydantic/pydantic-extra-types/pull/143) by [@07pepa](https://github.com/07pepa)
* 🔨 Update code formatting and linting configurations. PR [#144](https://github.com/pydantic/pydantic-extra-types/pull/144) by [@yezz123](https://github.com/yezz123)
* 👷 Add Python checking for dependencies. PR [#145](https://github.com/pydantic/pydantic-extra-types/pull/145) by [@yezz123](https://github.com/yezz123)
* 🐛 Fix single quote issue. PR [#148](https://github.com/pydantic/pydantic-extra-types/pull/148) by [@yezz123](https://github.com/yezz123)

## 2.5.0

* Add Pendulum DT support. PR [#110](https://github.com/pydantic/pydantic-extra-types/pull/110) by [@theunkn0wn1](https://github.com/theunkn0wn1)

## 2.4.1

* Fix refs blocking docs build. PR [#125](https://github.com/pydantic/pydantic-extra-types/pull/125) by [@sydney-runkle](https://github.com/sydney-runkle)

## 2.4.0

* Add: New type ISBN. PR [#116](https://github.com/pydantic/pydantic-extra-types/pull/116) by [lucasmucidas](https://github.com/lucasmucidas)
* Fix validate_digits actually allowing non-digit characters. PR [#120](https://github.com/pydantic/pydantic-extra-types/pull/120) by [romaincaillon](https://github.com/romaincaillon)
* Refactor the `validate_brand` method & add new types. PR [#56](https://github.com/pydantic/pydantic-extra-types/pull/56) by [yezz123](https://github.com/yezz123)
* Drop Python 3.7 & support 3.12. PR [#122](https://github.com/pydantic/pydantic-extra-types/pull/122) by [yezz123](https://github.com/yezz123)

## 2.3.0

* Upgrade pydantic version to >=2.5.2. PR [#113](https://github.com/pydantic/pydantic-extra-types/pull/113) by [hramezani](https://github.com/hramezani)

## 2.2.0

* Add `long` and `short` format to `as_hex`. PR [#93](https://github.com/pydantic/pydantic-extra-types/pull/93) by [DJRHails](https://github.com/DJRHails)
* Refactor documentation. PR [#98](https://github.com/pydantic/pydantic-extra-types/pull/98) by [Kludex](https://github.com/Kludex)
* Add `ULID` type. PR [#73](https://github.com/pydantic/pydantic-extra-types/pull/73) by [JeanArhancet](https://github.com/JeanArhancet)
* Add `__get_pydantic_json_schema__` method with `format='tel'`. PR [#106](https://github.com/pydantic/pydantic-extra-types/pull/106) by [hasansezertasan](https://github.com/hasansezertasan)

## 2.1.0

* Add `MacAddress` type. PR [#71](https://github.com/pydantic/pydantic-extra-types/pull/71) by [JeanArhancet](https://github.com/JeanArhancet)
* Fix usage of `MAC address`. PR [#72](https://github.com/pydantic/pydantic-extra-types/pull/72) by [yezz123](https://github.com/yezz123)
* Add docstrings for payment cards. PR [#77](https://github.com/pydantic/pydantic-extra-types/pull/77) by [tpdorsey](https://github.com/tpdorsey)
* Fix MAC address validation. PR [#79](https://github.com/pydantic/pydantic-extra-types/pull/79) by [JeanArhancet](https://github.com/JeanArhancet)
* Remove work in progress part from README.md. PR [#81](https://github.com/pydantic/pydantic-extra-types/pull/81) by [hramezani](https://github.com/hramezani)
* Add `Latitude`, `Longitude`, and `Coordinate`. PR [#76](https://github.com/pydantic/pydantic-extra-types/pull/76) by [JeanArhancet](https://github.com/JeanArhancet)
* Refactor: use stdlib and remove useless code. PR [#86](https://github.com/pydantic/pydantic-extra-types/pull/86) by [eumiro](https://github.com/eumiro)
* Make Latitude and Longitude evaluated. PR [#90](https://github.com/pydantic/pydantic-extra-types/pull/90) by [Kludex](https://github.com/Kludex)

## 2.0.0

* Migrate `Color` & `Payment Card`. PR [#2](https://github.com/pydantic/pydantic-extra-types/pull/2) by [yezz123](https://github.com/yezz123)
* Add `pydantic` to classifiers. PR [#13](https://github.com/pydantic/pydantic-extra-types/pull/13) by [yezz123](https://github.com/yezz123)
* Remove dependencies caching. PR [#16](https://github.com/pydantic/pydantic-extra-types/pull/16) by [yezz123](https://github.com/yezz123)
* Deprecate `__modify_schema__` method. PR [#20](https://github.com/pydantic/pydantic-extra-types/pull/20) by [yezz123](https://github.com/yezz123)
* Fix Color JSON schema generation. PR [#21](https://github.com/pydantic/pydantic-extra-types/pull/21) by [dmontagu](https://github.com/dmontagu)
* Fix issues of `pydantic_core.core_schema` has no attribute `xxx`. PR [#23](https://github.com/pydantic/pydantic-extra-types/pull/23) by [yezz123](https://github.com/yezz123)
* Fix Failed tests for `color` type. PR [#26](https://github.com/pydantic/pydantic-extra-types/pull/26) by [yezz123](https://github.com/yezz123)
* Created Country type. PR [#14](https://github.com/pydantic/pydantic-extra-types/pull/14) by [HomiGrotas](https://github.com/HomiGrotas)
* Add phone number types. PR [#25](https://github.com/pydantic/pydantic-extra-types/pull/25) by [JamesHutchison](https://github.com/JamesHutchison)
* Make `phonenumbers` a requirement. PR [#29](https://github.com/pydantic/pydantic-extra-types/pull/29) by [yezz123](https://github.com/yezz123)
* Add ABARouting number type. PR [#30](https://github.com/pydantic/pydantic-extra-types/pull/30) by [RevinderDev](https://github.com/RevinderDev)
* Add missing countries. PR [#32](https://github.com/pydantic/pydantic-extra-types/pull/32) by [EssaAlshammri](https://github.com/EssaAlshammri)
* Resolve `pydantic-core` dependency conflict. PR [#45](https://github.com/pydantic/pydantic-extra-types/pull/45) by [hirotasoshu](https://github.com/hirotasoshu)
* Add `MIR` card brand. PR [#46](https://github.com/pydantic/pydantic-extra-types/pull/46) by [hirotasoshu](https://github.com/hirotasoshu)
* Fix dependencies version. PR [#48](https://github.com/pydantic/pydantic-extra-types/pull/48) by [yezz123](https://github.com/yezz123)
* Add documentation for `Color` and `PaymentCardNumber`. PR [#50](https://github.com/pydantic/pydantic-extra-types/pull/50) by [Kludex](https://github.com/Kludex)
* Add hooky. PR [#51](https://github.com/pydantic/pydantic-extra-types/pull/51) by [Kludex](https://github.com/Kludex)
* Simplify project structure. PR [#52](https://github.com/pydantic/pydantic-extra-types/pull/52) by [Kludex](https://github.com/Kludex)
* Add coverage check on the pipeline. PR [#53](https://github.com/pydantic/pydantic-extra-types/pull/53) by [Kludex](https://github.com/Kludex)
* Refactor country type using `pycountry`. PR [#54](https://github.com/pydantic/pydantic-extra-types/pull/54) by [yezz123](https://github.com/yezz123)
* Add 100% coverage. PR [#57](https://github.com/pydantic/pydantic-extra-types/pull/57) by [Kludex](https://github.com/Kludex)
* Add support for transparent Color. PR [#59](https://github.com/pydantic/pydantic-extra-types/pull/59) by [CollinHeist](https://github.com/CollinHeist)
* Add documentation for `PhoneNumber` and `ABARoutingNumber`. PR [#60](https://github.com/pydantic/pydantic-extra-types/pull/60) by [Kludex](https://github.com/Kludex)
* Refactor README. PR [#61](https://github.com/pydantic/pydantic-extra-types/pull/61) by [Kludex](https://github.com/Kludex)
* Rename `routing_number.md` to `routing_numbers.md`. PR [#62](https://github.com/pydantic/pydantic-extra-types/pull/62) by [Kludex](https://github.com/Kludex)
* Fix code in `payment` documentation. PR [#63](https://github.com/pydantic/pydantic-extra-types/pull/63) by [yezz123](https://github.com/yezz123)
* Uprev pydantic to b3. PR [#69](https://github.com/pydantic/pydantic-extra-types/pull/69) by [samuelcolvin](https://github.com/samuelcolvin)
* Prepare for release 2.0.0. PR [#70](https://github.com/pydantic/pydantic-extra-types/pull/70) by [hramezani](https://github.com/hramezani)
