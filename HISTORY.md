# CHANGELOG

## v2.6.0

* Allow python-ulid 2.x on Python 3.9 and later by @musicinmybrain in <https://github.com/pydantic/pydantic-extra-types/pull/131>
* Do not pin the ”major” version of pycountry by @musicinmybrain in <https://github.com/pydantic/pydantic-extra-types/pull/132>
* 🤖 Create dependabot.yml for updating GitHub action by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/134>
* :memo: Refactor Documentation for ISBN and MAC address modules by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/124>
* Add language code definitions and test by @07pepa in <https://github.com/pydantic/pydantic-extra-types/pull/141>
* :memo: Create a `changelog` to match release notes by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/142>
* Add currency code ISO 4217 and its subset that includes only currencies by @07pepa in <https://github.com/pydantic/pydantic-extra-types/pull/143>
* 🔨 Update code formatting and linting configurations by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/144>
* 👷 Add Python checking for dependencies by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/145>
* 🐛 fix single quote issue  by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/148>

## v2.5.0

* Add Pendulum DT support by @theunkn0wn1 in <https://github.com/pydantic/pydantic-extra-types/pull/110>

## v2.4.1

* Fix refs blocking docs build by @sydney-runkle in <https://github.com/pydantic/pydantic-extra-types/pull/125>

## v2.4.0

* Add: New type ISBN by @lucasmucidas in <https://github.com/pydantic/pydantic-extra-types/pull/116>
* fix validate_digits actually allowing non digit characters by @romaincaillon in <https://github.com/pydantic/pydantic-extra-types/pull/120>
* ♻️ refactor the `validate_brand` method & add new types by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/56>
* ✅ Drop python 3.7 & support 3.12 by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/122>

## v2.3.0

* Upgrade pydantic version to >=2.5.2 by @hramezani in <https://github.com/pydantic/pydantic-extra-types/pull/113>

## v.2.2.0

* Add `long` and `short` format to `as_hex` by @DJRHails in <https://github.com/pydantic/pydantic-extra-types/pull/93>
* Refactor documentation by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/98>
* ✨  add `ULID` type by @JeanArhancet in <https://github.com/pydantic/pydantic-extra-types/pull/73>
* Added `__get_pydantic_json_schema__` method with `format='tel'` by @hasansezertasan in <https://github.com/pydantic/pydantic-extra-types/pull/106>

## v2.1.0

* ✨  add `MacAddress` type by @JeanArhancet in <https://github.com/pydantic/pydantic-extra-types/pull/71>
* :memo: fix usage of `MAC address` by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/72>
* Add docstrings for payment cards by @tpdorsey in <https://github.com/pydantic/pydantic-extra-types/pull/77>
* Fix mac adddress validation by @JeanArhancet in <https://github.com/pydantic/pydantic-extra-types/pull/79>
* Remove work in progress part from README.md by @hramezani in <https://github.com/pydantic/pydantic-extra-types/pull/81>
* Add `Latitude`, `Longitude` and `Coordinate`  by @JeanArhancet in <https://github.com/pydantic/pydantic-extra-types/pull/76>
* Refactor: use stdlib and remove useless code by @eumiro in <https://github.com/pydantic/pydantic-extra-types/pull/86>
* Make Latitude and Longitude evaluated by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/90>

## v2.0.0

* Migrate `Color` & `Payment Card` by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/2>
* add `pydantic` to classifiers by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/13>
* remove dependencies caching by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/16>
* :bug: deprecate `__modify_schema__` method by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/20>
* Fix Color JSON schema generation by @dmontagu in <https://github.com/pydantic/pydantic-extra-types/pull/21>
* fix issues of `pydantic_core.core_schema` has no attribute `xxx` by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/23>
* Fix Failed tests for `color` type by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/26>
* Created Country type by @HomiGrotas in <https://github.com/pydantic/pydantic-extra-types/pull/14>
* Add phone number types by @JamesHutchison in <https://github.com/pydantic/pydantic-extra-types/pull/25>
* make `phonenumbers` a requirement by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/29>
* chore(feat): Add ABARouting number type by @RevinderDev in <https://github.com/pydantic/pydantic-extra-types/pull/30>
* add missing countries by @EssaAlshammri in <https://github.com/pydantic/pydantic-extra-types/pull/32>
* chore: resolve `pydantic-core` dependency conflict by @hirotasoshu in <https://github.com/pydantic/pydantic-extra-types/pull/45>
* Add `MIR` card brand by @hirotasoshu in <https://github.com/pydantic/pydantic-extra-types/pull/46>
* fix dependencies version by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/48>
* 📝 Add documentation for `Color` and `PaymentCardNumber` by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/50>
* Add hooky by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/51>
* ♻️ Simplify project structure by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/52>
* 👷 Add coverage check on the pipeline by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/53>
* ♻️ refactor country type using `pycountry` by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/54>
* ✅ Add 100% coverage by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/57>
* Add support for transparent Color by @CollinHeist in <https://github.com/pydantic/pydantic-extra-types/pull/59>
* 📝 Add documentation for `PhoneNumber` and `ABARoutingNumber` by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/60>
* 📝 Refactor README by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/61>
* 🚚 Rename `routing_number.md` to `routing_numbers.md` by @Kludex in <https://github.com/pydantic/pydantic-extra-types/pull/62>
* :memo: fix code in `payment` documentation by @yezz123 in <https://github.com/pydantic/pydantic-extra-types/pull/63>
* uprev pydantic to b3 by @samuelcolvin in <https://github.com/pydantic/pydantic-extra-types/pull/69>
* Prepare for release 2.0.0 by @hramezani in <https://github.com/pydantic/pydantic-extra-types/pull/70>
