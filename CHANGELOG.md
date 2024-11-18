# ozi-core CHANGELOG
## 1.5.9 (2024-11-18)


### Build system


* build(deps): ozi-spec~=0.12.1 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`8d59810`](https://github.com/OZI-Project/ozi-core/commit/8d598109c29e7e57a016f7273afa771815097ea6))

* build(deps): update ozi-templates requirement from ~=2.14.0 to ~=2.15.0

Updates the requirements on [ozi-templates](https://github.com/OZI-Project/ozi-templates) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-templates/releases)
- [Changelog](https://github.com/OZI-Project/ozi-templates/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-templates/compare/2.14.0...2.15.0)


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`43ffac1`](https://github.com/OZI-Project/ozi-core/commit/43ffac13c1182878b39d4885c3531db1f0612d91))

## 1.5.8 (2024-11-17)


### Bug fixes


* fix: read user config on ozi-fix interactive prompt __init__ — rjdbcm <rjdbcm@outlook.com>
([`c925813`](https://github.com/OZI-Project/ozi-core/commit/c9258138c14260679f717cb55b262faca6dc7cbf))

## 1.5.7 (2024-11-17)


### Bug fixes


* fix: setting pretty in interactive mode ozi-fix works — rjdbcm <rjdbcm@outlook.com>
([`01182ec`](https://github.com/OZI-Project/ozi-core/commit/01182ec339fda7a124c1e41192423b092aa149e7))

## 1.5.6 (2024-11-17)


### Bug fixes


* fix: pretty mode setting works in ozi-fix interactive — rjdbcm <rjdbcm@outlook.com>
([`0da3aa4`](https://github.com/OZI-Project/ozi-core/commit/0da3aa452cfb49d7b0f57dfa9e4cb7fe5debc9b1))

## 1.5.5 (2024-11-17)


### Bug fixes


* fix: update deadline for flaky test — rjdbcm <rjdbcm@outlook.com>
([`f5f7b68`](https://github.com/OZI-Project/ozi-core/commit/f5f7b68e215a0de8f06403644398ed6591ab4fef))

* fix: correctly loop fix mode interactive dialog — rjdbcm <rjdbcm@outlook.com>
([`bea79f0`](https://github.com/OZI-Project/ozi-core/commit/bea79f005be28a32c9c5b7b9bd346d78a903e8c2))

* fix: remove generated locales file used for testing — rjdbcm <rjdbcm@outlook.com>
([`bd646fd`](https://github.com/OZI-Project/ozi-core/commit/bd646fdb518e2a973d4a11718822e936a29d8823))

* fix: translate fix mode dialog ok button — rjdbcm <rjdbcm@outlook.com>
([`a20fd2a`](https://github.com/OZI-Project/ozi-core/commit/a20fd2a8c4a1f51820a4be76f190c05a8139260f))

## 1.5.4 (2024-11-17)


### Bug fixes


* fix: use the user-defined language locale in interactive prompts — rjdbcm <rjdbcm@outlook.com>
([`c691377`](https://github.com/OZI-Project/ozi-core/commit/c691377662f361acb9e4b0af0a4df69a9aa604b7))

## 1.5.3 (2024-11-17)


### Bug fixes


* fix: add options menu to set ozi-fix options and menu language — rjdbcm <rjdbcm@outlook.com>
([`c1d5206`](https://github.com/OZI-Project/ozi-core/commit/c1d520689c07470fb3830106948871ae61991ff0))


### Unknown


* run lint — rjdbcm <rjdbcm@outlook.com>
([`d6f07e8`](https://github.com/OZI-Project/ozi-core/commit/d6f07e8914c7331ca176da326ce01aaba5495f38))

## 1.5.2 (2024-11-17)


### Bug fixes


* fix: add translated string for options save dialog
([`fb43c37`](https://github.com/OZI-Project/ozi-core/commit/fb43c378b4de29e165642756222bd67c51fe008a))

## 1.5.1 (2024-11-17)


### Bug fixes


* fix: remove __init__ from dataclasses in stubs — rjdbcm <rjdbcm@outlook.com>
([`49f1889`](https://github.com/OZI-Project/ozi-core/commit/49f1889b70ca831c08f9e15e5fa84a9300bb1a49))

* fix: run black — rjdbcm <rjdbcm@outlook.com>
([`f8098bd`](https://github.com/OZI-Project/ozi-core/commit/f8098bdd10387fba138b4d8c818dcadc741370b3))

* fix: clean up stubs — rjdbcm <rjdbcm@outlook.com>
([`0ec4271`](https://github.com/OZI-Project/ozi-core/commit/0ec42713adbeead137520dd74d3069af7b6af542))


### Performance improvements


* perf: add config.yml file for user-defined defaults in interactive CLI — rjdbcm <rjdbcm@outlook.com>
([`0dbfdd5`](https://github.com/OZI-Project/ozi-core/commit/0dbfdd5ea895254a378f19ac289f61de623241e3))

## 1.5.0 (2024-11-15)


### Build system


* build(deps): bump OZI-Project/release from 1.0.4 to 1.0.5

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 1.0.4 to 1.0.5.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/74350f112641257ed33f06f83c3e6fc7ae92059b...1a3cb28a9a9d51fa8e333740a8b863c0f23ab3da)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`8d7d27c`](https://github.com/OZI-Project/ozi-core/commit/8d7d27ced4955f2fa02a78c22c5b43c72630227e))

* build(deps): bump OZI-Project/draft from 1.4.0 to 1.5.0

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 1.4.0 to 1.5.0.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/1.4.0...1.5.0)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`5f54cbf`](https://github.com/OZI-Project/ozi-core/commit/5f54cbf521937e973130ce289518768fc0235815))

* build(deps): bump OZI-Project/publish from 1.4.1 to 1.5.0

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.4.1 to 1.5.0.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.4.1...1.5.0)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`a6b118d`](https://github.com/OZI-Project/ozi-core/commit/a6b118d93840e36b0ec29ae9da9fa3672a62f45b))

* build(deps): bump OZI-Project/checkpoint from 1.1.3 to 1.2.1

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.1.3 to 1.2.1.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.1.3...1.2.1)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`d9bea4e`](https://github.com/OZI-Project/ozi-core/commit/d9bea4e2a6a7f09d07519d24ab25d97cfbb64d61))

* build(deps): update ozi-templates requirement from ~=2.13.15 to ~=2.14.0

Updates the requirements on [ozi-templates](https://github.com/OZI-Project/ozi-templates) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-templates/releases)
- [Changelog](https://github.com/OZI-Project/ozi-templates/blob/2.14.0/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-templates/compare/2.13.15...2.14.0)


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`e0ea88e`](https://github.com/OZI-Project/ozi-core/commit/e0ea88ea423613534a303b1cdd26ec61477b450e))


### Features


* feat: spec v0.12 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`04c270c`](https://github.com/OZI-Project/ozi-core/commit/04c270c2b4c03b7976352d460097ce89c84c9629))

## 1.4.17 (2024-11-15)


### Build system


* build(deps): update ozi-spec requirement from ~=0.11.7 to ~=0.12.0

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/0.12.0/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.11.7...0.12.0)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`352f207`](https://github.com/OZI-Project/ozi-core/commit/352f2074489dcc66a605c898f7d1e2eb8f3dd30a))

* build(deps): ozi-spec~=0.11.7 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`8a00811`](https://github.com/OZI-Project/ozi-core/commit/8a008116bcac9831e43a4a7e8d0e07901b408bf0))

## 1.4.16 (2024-11-11)


### Build system


* build(deps): ozi-templates~=2.13.15 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`fce5480`](https://github.com/OZI-Project/ozi-core/commit/fce5480cbba4a5907613425d100696423fae0dc0))

* build: fix tox paths for cross-platform — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`3025862`](https://github.com/OZI-Project/ozi-core/commit/3025862a16456129d6a8826b8c658c5613afbaad))

* build(deps): bump OZI-Project/checkpoint from 1.1.2 to 1.1.3

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.1.2 to 1.1.3.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.1.2...1.1.3)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`f75506d`](https://github.com/OZI-Project/ozi-core/commit/f75506d5eeb81335f2b9025cbf4b02193e52e7f6))

* build(deps): bump OZI-Project/checkpoint from 1.1.1 to 1.1.2

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.1.1 to 1.1.2.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.1.1...1.1.2)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`74a7c20`](https://github.com/OZI-Project/ozi-core/commit/74a7c207c31541ab5cc24117b710c9ebd0422240))

* build:  create dev.yml checkpoints for CI — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`8c3b9a5`](https://github.com/OZI-Project/ozi-core/commit/8c3b9a546b222806b5862653487dd68603b80edc))

## 1.4.15 (2024-11-11)


### Performance improvements


* perf(ozi-fix): add input validation — rjdbcm <rjdbcm@outlook.com>
([`364eb12`](https://github.com/OZI-Project/ozi-core/commit/364eb12b585d5ce077bb8fc03b6c7bcf1e8e085d))

## 1.4.14 (2024-11-10)


### Build system


* build(deps): ozi-templates~=2.13.14 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`c5c5cc3`](https://github.com/OZI-Project/ozi-core/commit/c5c5cc3bb80b50ed4b2233f0a11d82020cde289f))

## 1.4.13 (2024-11-10)


### Bug fixes


* fix: render.build_child ignores errors on existing directory — rjdbcm <rjdbcm@outlook.com>
([`1049e9a`](https://github.com/OZI-Project/ozi-core/commit/1049e9ae6d31cf51a7f8c0000779ee82f2eb02cf))

* fix: revert to OZI-Project/publish 1.4.1 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`a64f4f5`](https://github.com/OZI-Project/ozi-core/commit/a64f4f56db2ee423a2198e142837f3c78bbeadde))


### Build system


* build(deps): ozi-templates~=2.13.13 — rjdbcm <rjdbcm@outlook.com>
([`c493822`](https://github.com/OZI-Project/ozi-core/commit/c493822352e08bc0a36dc10afff8fca6f1ffc88a))


### Performance improvements


* perf: meson rewriter compatibility improvements — rjdbcm <rjdbcm@outlook.com>
([`8a96beb`](https://github.com/OZI-Project/ozi-core/commit/8a96beb0a06fbc6ca257b4164634b78e6460fa19))

## 1.4.12 (2024-11-09)


### Build system


* build(deps): bump OZI-Project/publish from 1.4.1 to 1.4.2

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.4.1 to 1.4.2.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.4.1...1.4.2)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`b00567d`](https://github.com/OZI-Project/ozi-core/commit/b00567d6cd6ed16c34751610849272affd066cdd))


### Performance improvements


* perf(ozi-fix interactive): ability to input files and folders — rjdbcm <rjdbcm@outlook.com>
([`c832796`](https://github.com/OZI-Project/ozi-core/commit/c832796b96e5bc3668a6ff5863b95e4fcf3e2245))

## 1.4.11 (2024-11-08)


### Performance improvements


* perf(ozi-fix): unroll ``meson.build`` subdir call loops before outputting rewriter commands — rjdbcm <rjdbcm@outlook.com>
([`5f71978`](https://github.com/OZI-Project/ozi-core/commit/5f719785602b18b674729f514125caf6e7f3f007))

## 1.4.10 (2024-11-07)


### Performance improvements


* perf(ozi-fix interactive): automatic meson rewriter invocation — rjdbcm <rjdbcm@outlook.com>
([`ea6a4be`](https://github.com/OZI-Project/ozi-core/commit/ea6a4be3b535036f27d77c543a8d09ea15c1446a))

* perf: OZI 1.24 wrapfile — rjdbcm <rjdbcm@outlook.com>
([`7cf1644`](https://github.com/OZI-Project/ozi-core/commit/7cf164432c391cfe0c2f9fbae40e00f43b8d447c))


### Unknown


* lint: run isort — rjdbcm <rjdbcm@outlook.com>
([`7118775`](https://github.com/OZI-Project/ozi-core/commit/7118775bcb2d5ac238450b42904b8bce53d44e0d))

## 1.4.9 (2024-11-07)


### Bug fixes


* fix: ozi-templates~=2.13.11 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`cbea6d8`](https://github.com/OZI-Project/ozi-core/commit/cbea6d8c8f6105fe9750932cfde8dd286293fd31))

* fix: ozi-spec 0.11.5 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`43feb7b`](https://github.com/OZI-Project/ozi-core/commit/43feb7bf31fdd8fb065cb9b4272ed5be202b4a90))


### Build system


* build(deps): bump OZI-Project/publish from 1.4.0 to 1.4.1

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.4.0 to 1.4.1.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.4.0...1.4.1)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`4b23f06`](https://github.com/OZI-Project/ozi-core/commit/4b23f0655ceb2fcd0052d90aedb12757a6e485ad))

## 1.4.8 (2024-11-04)


### Bug fixes


* fix: correct ui submodule install path — rjdbcm <rjdbcm@outlook.com>
([`f9f0969`](https://github.com/OZI-Project/ozi-core/commit/f9f0969a4e9b897f1f9c223f8ab316bd651e69c1))

## 1.4.7 (2024-11-04)


### Performance improvements


* perf: add translated strings to ozi-fix interactive — rjdbcm <rjdbcm@outlook.com>
([`ac1f0e6`](https://github.com/OZI-Project/ozi-core/commit/ac1f0e63c0711e45548a304f517b00c2e5799b92))

* perf: fix.build_definition.walk function now a generator — rjdbcm <rjdbcm@outlook.com>
([`86385ad`](https://github.com/OZI-Project/ozi-core/commit/86385ad0af04a619a8d8152545fa6fd4dd8cf39d))

* perf: refactor UI to add an ozi-fix interactive mode — rjdbcm <rjdbcm@outlook.com>
([`980831d`](https://github.com/OZI-Project/ozi-core/commit/980831d967ce3067bec5c8a8e5e3b24632990c7d))


### Unknown


* :hammer: refactor UI to add an ozi-fix interactive mode — rjdbcm <rjdbcm@outlook.com>
([`4734d92`](https://github.com/OZI-Project/ozi-core/commit/4734d9279656cbbceff075c385e7f3e951e48817))

## 1.4.6 (2024-11-01)


### Build system


* build(endpoints): add sigstore urls to allow list — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`7912ae8`](https://github.com/OZI-Project/ozi-core/commit/7912ae89c67d1a0ff76dea4da81241e7e96d7c8e))

* build(deps): ozi-templates~=2.13.8 — rjdbcm <rjdbcm@outlook.com>
([`142da4a`](https://github.com/OZI-Project/ozi-core/commit/142da4a639b7286611a5340da2673ec7fd28da80))


### Performance improvements


* perf: test that harden-runner blocks render — rjdbcm <rjdbcm@outlook.com>
([`32544ad`](https://github.com/OZI-Project/ozi-core/commit/32544ad35f7e759e188c8e6a9b1d44c0b7c7cd22))

## 1.4.5 (2024-10-29)


### Build system


* build(deps): ozi-spec~=0.11.4 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`7102f08`](https://github.com/OZI-Project/ozi-core/commit/7102f08f234d4db97bbb48a977b644c59e3106b6))

## 1.4.4 (2024-10-28)


### Build system


* build(deps): ozi-spec~=0.11.2 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`e74e7b9`](https://github.com/OZI-Project/ozi-core/commit/e74e7b9b7f61d6fbc24706f8b3bca0f8e2bc7381))

## 1.4.3 (2024-10-28)


### Bug fixes


* fix: only use multiline input_dialog for copyright header — rjdbcm <rjdbcm@outlook.com>
([`df89a10`](https://github.com/OZI-Project/ozi-core/commit/df89a10bedf867264e29cb6803017f3e532827d7))


### Build system


* build(deps): update ozi-templates requirement from ~=2.12.5 to ~=2.13.0

Updates the requirements on [ozi-templates](https://github.com/OZI-Project/ozi-templates) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-templates/releases)
- [Changelog](https://github.com/OZI-Project/ozi-templates/blob/2.13.0/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-templates/compare/2.12.5...2.13.0)


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`719ccea`](https://github.com/OZI-Project/ozi-core/commit/719ccea81f271427e318ce8bc7e32f094b97a44c))

* build(deps): bump OZI-Project/checkpoint from 1.0.2 to 1.1.1

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.0.2 to 1.1.1.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.0.2...1.1.1)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`8d85692`](https://github.com/OZI-Project/ozi-core/commit/8d8569240db9a9df177e3efc6b6fc55d6b3eabc4))

## 1.4.2 (2024-10-25)


### Build system


* build: update fallback version to 1.24 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`465dd5d`](https://github.com/OZI-Project/ozi-core/commit/465dd5d767799c7669835f1fafd8a2688ded89e4))

## 1.4.1 (2024-10-25)


### Bug fixes


* fix: ozi-spec~=0.11.1

OZI-Project/checkpoint 1.1.1 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`5763687`](https://github.com/OZI-Project/ozi-core/commit/5763687061a3bb7027defa61ccd2873622233350))

## 1.4.0 (2024-10-25)


### Bug fixes


* fix: generate locales at build time — rjdbcm <rjdbcm@outlook.com>
([`83e3c40`](https://github.com/OZI-Project/ozi-core/commit/83e3c401f35d644de406db9668e1265301096fe7))

* fix: generate locales at build time — rjdbcm <rjdbcm@outlook.com>
([`b481dc7`](https://github.com/OZI-Project/ozi-core/commit/b481dc7201c145cd5edf90ee0e911169dac47a5c))


### Features


* feat: ozi-spec~=0.11.0 — rjdbcm <rjdbcm@outlook.com>
([`f78d693`](https://github.com/OZI-Project/ozi-core/commit/f78d69391998f795de987595680bb6d22a68a8fb))

## 1.3.7 (2024-10-24)


### Bug fixes


* fix: update fallback version to 1.23 — rjdbcm <rjdbcm@outlook.com>
([`1de7c4a`](https://github.com/OZI-Project/ozi-core/commit/1de7c4a8855b647b3844896f9af4632467382002))


### Performance improvements


* perf: TAP-Producer~=1.4.1 and remove undocumented dependency on typing_extensions <3.11 — rjdbcm <rjdbcm@outlook.com>
([`8bba66c`](https://github.com/OZI-Project/ozi-core/commit/8bba66c96f0ba008cb878f4a29ccd2a007ba8342))

## 1.3.6 (2024-10-19)


### Bug fixes


* fix: dont print TAP plan after dumping json — rjdbcm <rjdbcm@outlook.com>
([`bc68a76`](https://github.com/OZI-Project/ozi-core/commit/bc68a76cf05c3f9e16f9c2ac63ebb611858ac686))

## 1.3.5 (2024-10-19)


### Bug fixes


* fix(ozi-fix): correctly suppress TAP output — rjdbcm <rjdbcm@outlook.com>
([`ac53fe7`](https://github.com/OZI-Project/ozi-core/commit/ac53fe73f1e9ca74b894300fdd2a7b54feb65395))

## 1.3.4 (2024-10-18)


### Build system


* build(deps): bump OZI-Project/draft from 1.3.0 to 1.4.0

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 1.3.0 to 1.4.0.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/1.3.0...1.4.0)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`ea0e895`](https://github.com/OZI-Project/ozi-core/commit/ea0e8958ccea055c5dcf880df7088774a9c8015c))

* build(deps): bump OZI-Project/publish from 1.3.0 to 1.4.0

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.3.0 to 1.4.0.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.3.0...1.4.0)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`9a5d860`](https://github.com/OZI-Project/ozi-core/commit/9a5d86011ef5fbb434787264a98d2452fcc68556))

* build(deps): ozi-spec~=0.10.8 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`81e9f2e`](https://github.com/OZI-Project/ozi-core/commit/81e9f2efa683ea5ee74ce54d75229209c33e3882))

* build(deps): TAP-Producer~=1.3.2 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`fcf69fd`](https://github.com/OZI-Project/ozi-core/commit/fcf69fd07da3f053ce74d506c4c185fb82d5b531))

## 1.3.3 (2024-10-18)


### Bug fixes


* fix: correct API use for TAP-Producer 1.3 — rjdbcm <rjdbcm@outlook.com>
([`2207a29`](https://github.com/OZI-Project/ozi-core/commit/2207a29982b2b592249f625772e76a981a2f5cfe))


### Build system


* build(deps): TAP-Producer~=1.3.0 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`b58e477`](https://github.com/OZI-Project/ozi-core/commit/b58e4777804e4082a279d05560ba5db16e6c01fd))

## 1.3.2 (2024-10-16)


### Bug fixes


* fix: correct TAP output, README symlink

TAP-Producer 1.2.0 — rjdbcm <rjdbcm@outlook.com>
([`127c7b2`](https://github.com/OZI-Project/ozi-core/commit/127c7b2c3f121ecadbe78d92390c65ff179d5bed))

## 1.3.1 (2024-10-14)


### Bug fixes


* fix: ozi-spec~=0.10.7

OZI version 1.23 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`339625f`](https://github.com/OZI-Project/ozi-core/commit/339625f76951eea5d24bac09597f75d60787f4b7))

## 1.3.0 (2024-10-14)


### Build system


* build(deps): bump OZI-Project/release from 1.0.3 to 1.0.4

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 1.0.3 to 1.0.4.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/d764d82aa0900effc1590b0281ff35d67be592fd...74350f112641257ed33f06f83c3e6fc7ae92059b)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`bbe3ff6`](https://github.com/OZI-Project/ozi-core/commit/bbe3ff6fde69878c187f3c4c34d1ddcddc82ca73))

* build(deps): bump OZI-Project/checkpoint from 1.0.1 to 1.0.2

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.0.1 to 1.0.2.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.0.1...1.0.2)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`0d78a34`](https://github.com/OZI-Project/ozi-core/commit/0d78a34c18ebea6870f4202151f8971f5c8be10b))

* build(deps): bump OZI-Project/publish from 1.1.0 to 1.3.0

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.1.0 to 1.3.0.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.1.0...1.3.0)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`f81c824`](https://github.com/OZI-Project/ozi-core/commit/f81c824ff7684aa2ad8c4b6b5ec79c293f80e920))

* build(deps): bump OZI-Project/draft from 1.1.0 to 1.3.0

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 1.1.0 to 1.3.0.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/1.1.0...1.3.0)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`5349a29`](https://github.com/OZI-Project/ozi-core/commit/5349a299185b033eb907ac6f66282ed5e011d6f6))


### Features


* feat: semantic-release 9.10 and complete typing stubs — rjdbcm <rjdbcm@outlook.com>
([`bd1b317`](https://github.com/OZI-Project/ozi-core/commit/bd1b3172683cb81e4329422d99fd9103d10c0782))

* feat: semantic-release 9.11 and complete typing stubs — rjdbcm <rjdbcm@outlook.com>
([`ca12220`](https://github.com/OZI-Project/ozi-core/commit/ca12220749c93f6f7dbbf43c2dfa7d1e32c80843))

## 1.2.17 (2024-10-14)


### Performance improvements


* perf: correct stub typechecking — rjdbcm <rjdbcm@outlook.com>
([`b6d7656`](https://github.com/OZI-Project/ozi-core/commit/b6d7656c945767619173f2f6026b8a97dafbf825))

* perf: add stubfiles
([`743c9e8`](https://github.com/OZI-Project/ozi-core/commit/743c9e8c06d4272f5b05be8bff368fd016109a14))

* perf: add stubfiles — rjdbcm <rjdbcm@outlook.com>
([`d97b1fb`](https://github.com/OZI-Project/ozi-core/commit/d97b1fb43ea808dcac5e1c7bfd53697cb0a24a85))

## 1.2.16 (2024-10-13)


### Bug fixes


* fix: temporarily disable automated build time locale generation — rjdbcm <rjdbcm@outlook.com>
([`efa70de`](https://github.com/OZI-Project/ozi-core/commit/efa70de173e94ead61e2fddeaf5b17853e8e3a13))


### Performance improvements


* perf: better copyright header parsing — rjdbcm <rjdbcm@outlook.com>
([`5a63060`](https://github.com/OZI-Project/ozi-core/commit/5a63060b3b8796672f9388d173c980c47b64ed60))

* perf: refresh locales at build time, fix some typos — rjdbcm <rjdbcm@outlook.com>
([`ebad03f`](https://github.com/OZI-Project/ozi-core/commit/ebad03ff899ede4aad6159a96fabd547a2784b99))


### Unknown


* :globe_with_meridians:(ozi-fix): internationalize the TAP output — rjdbcm <rjdbcm@outlook.com>
([`4465a05`](https://github.com/OZI-Project/ozi-core/commit/4465a05bfa66e3ac24944f5b48c3b85ce0f8f6b5))

* :globe_with_meridians:(ozi-new): internationalize the TAP output — rjdbcm <rjdbcm@outlook.com>
([`02437ee`](https://github.com/OZI-Project/ozi-core/commit/02437eea3aa02198c736380080627fd2d0f52d24))

* :hammer: refactor interactive dialogs
([`13a2846`](https://github.com/OZI-Project/ozi-core/commit/13a284682ff53b5eef0632b4b68606e2d58a5cd8))

## 1.2.15 (2024-10-10)


### Bug fixes


* fix: default to english locale in case of unsupported language — rjdbcm <rjdbcm@outlook.com>
([`d41ed78`](https://github.com/OZI-Project/ozi-core/commit/d41ed783972f6f64d14014a783e52b14fc85d130))

* fix: incorrect/missing translation asset keys
([`9b34997`](https://github.com/OZI-Project/ozi-core/commit/9b349970c4d4d6031473e184e9fbf5953ee93a61))

## 1.2.14 (2024-10-09)


### Bug fixes


* fix: missing help text for target — rjdbcm <rjdbcm@outlook.com>
([`a3a8b7b`](https://github.com/OZI-Project/ozi-core/commit/a3a8b7b8443b2c8b07d66dd2db01954984b52674))

## 1.2.13 (2024-10-09)

## 1.2.12 (2024-10-09)

## 1.2.11 (2024-10-08)


### Bug fixes


* fix: hard locale file for the time being — rjdbcm <rjdbcm@outlook.com>
([`e7285e8`](https://github.com/OZI-Project/ozi-core/commit/e7285e884e12b49b78121851a1cd10ebfb8f28ea))

* fix: install PyYAML during build — rjdbcm <rjdbcm@outlook.com>
([`8b7c5f9`](https://github.com/OZI-Project/ozi-core/commit/8b7c5f9dbf0b9cec467c0ff17e1fd744f18caabd))

* fix: lint complaints — rjdbcm <rjdbcm@outlook.com>
([`eb2fd82`](https://github.com/OZI-Project/ozi-core/commit/eb2fd8259c59771a478e186791bf218d15569ff4))

* fix: type locale data — rjdbcm <rjdbcm@outlook.com>
([`a55512d`](https://github.com/OZI-Project/ozi-core/commit/a55512d5af8750e96cdc71752d1f3a94a282a736))

* fix: locales are now pre-compiled - fixes issue with docs display — rjdbcm <rjdbcm@outlook.com>
([`5ee0203`](https://github.com/OZI-Project/ozi-core/commit/5ee020302e254ea48a342c279632ddd245d68c61))


### Performance improvements


* perf: ozi-spec~=0.10.2 semantic-release v9.9 — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`d1c8b55`](https://github.com/OZI-Project/ozi-core/commit/d1c8b555de58bd3c851b2f4dcd786b24c7eddb86))


### Unknown


* Update LICENSE.txt to include exception text — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`3f49071`](https://github.com/OZI-Project/ozi-core/commit/3f490717aa4c96818ac3a333b2288059eae28a54))

## 1.2.10 (2024-10-08)


### Bug fixes


* fix: add no cover to import guard — rjdbcm <rjdbcm@outlook.com>
([`efc9a16`](https://github.com/OZI-Project/ozi-core/commit/efc9a163057a61fd4026f191fab683a98c95715d))


### Performance improvements


* perf: add import guard for curses on win32
([`5816226`](https://github.com/OZI-Project/ozi-core/commit/58162268fbd74992e91726a41d24020e5f61ef36))

* perf: add import guard for curses on win32 — rjdbcm <rjdbcm@outlook.com>
([`52d1a3f`](https://github.com/OZI-Project/ozi-core/commit/52d1a3f3810e125466f8d7e5581b5008658b791b))

* perf: chinese UI title more readable — rjdbcm <rjdbcm@outlook.com>
([`089a5df`](https://github.com/OZI-Project/ozi-core/commit/089a5dfcff7d8ce0e6db7bc4022219b88b2e766a))

* perf(ozi-new): import guard in case of win32 — rjdbcm <rjdbcm@outlook.com>
([`155eda0`](https://github.com/OZI-Project/ozi-core/commit/155eda09e02bb63dd720ababf257934037b528df))

* perf: set raw terminal mode for interactive prompt — rjdbcm <rjdbcm@outlook.com>
([`1a37bc7`](https://github.com/OZI-Project/ozi-core/commit/1a37bc7b30d56ef3f15936c8a26d1b59caf5385c))

* perf: flexible input dialog width and height based on default — rjdbcm <rjdbcm@outlook.com>
([`e9ae813`](https://github.com/OZI-Project/ozi-core/commit/e9ae813e861fb4144c7bf1a75ff98e1bb17c707e))

## 1.2.9 (2024-10-07)


### Bug fixes


* fix: add License-File dialog — rjdbcm <rjdbcm@outlook.com>
([`aed82bc`](https://github.com/OZI-Project/ozi-core/commit/aed82bcda0749919824ca22a3644b5e5b27e1821))


### Performance improvements


* perf: remove LicenseFileValidator — rjdbcm <rjdbcm@outlook.com>
([`c446f4e`](https://github.com/OZI-Project/ozi-core/commit/c446f4e2f74c0a6e0c193f7831f5846647bb54bd))

* perf: better Chinese UX — rjdbcm <rjdbcm@outlook.com>
([`bf64f1b`](https://github.com/OZI-Project/ozi-core/commit/bf64f1bed7b74c9e1134b46f22450b14c378761a))

* perf: fix missing title translation — rjdbcm <rjdbcm@outlook.com>
([`db02db5`](https://github.com/OZI-Project/ozi-core/commit/db02db51da361172966eae038095abec3c19abfa))

## 1.2.8 (2024-10-07)


### Performance improvements


* perf: clean up interactive prompt implementation — rjdbcm <rjdbcm@outlook.com>
([`6a1a86b`](https://github.com/OZI-Project/ozi-core/commit/6a1a86b3addc391b103556d7281379451242253a))

## 1.2.7 (2024-10-06)


### Bug fixes


* fix: empty translation values coerced to str — rjdbcm <rjdbcm@outlook.com>
([`f1f14eb`](https://github.com/OZI-Project/ozi-core/commit/f1f14eb1daedd21d156faaed0826d4ffe1e09d1d))

## 1.2.6 (2024-10-06)


### Bug fixes


* fix: add some pyright ignores — rjdbcm <rjdbcm@outlook.com>
([`a80f17f`](https://github.com/OZI-Project/ozi-core/commit/a80f17fa5ca11dfc91eeb778fc3dd8ac2832e930))


### Performance improvements


* perf: more translations for the CLI — rjdbcm <rjdbcm@outlook.com>
([`95ea579`](https://github.com/OZI-Project/ozi-core/commit/95ea579211f14e9ac1a4378af396ec3ccdae67a1))

## 1.2.5 (2024-10-05)


### Bug fixes


* fix: remove 3.10 checkpoint pending deprecation — Eden Ross Duff, MSc, DDiv <rjdbcm@outlook.com>
([`69f1ef9`](https://github.com/OZI-Project/ozi-core/commit/69f1ef9f0164eaeb04f6a393b719c6a2fdcc7876))

* fix: erroneous call to TAP version after interactive session — rjdbcm <rjdbcm@outlook.com>
([`a03be5f`](https://github.com/OZI-Project/ozi-core/commit/a03be5f76fa04146ed6947f932724741bc38aa1c))


### Build system


* build(deps): bump OZI-Project/release from 1.0.2 to 1.0.3

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 1.0.2 to 1.0.3.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/48fdd720e637c583fe162559ebe23d5ae0e24f8f...d764d82aa0900effc1590b0281ff35d67be592fd)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`a1289cd`](https://github.com/OZI-Project/ozi-core/commit/a1289cd42100f470ba19b771c5cd71aba7365f31))

* build(deps): bump OZI-Project/release from 1.0.1 to 1.0.2

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 1.0.1 to 1.0.2.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/3015ae773cba4b74f1ff7afb55ad1e6324d56f51...48fdd720e637c583fe162559ebe23d5ae0e24f8f)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`ae1a78e`](https://github.com/OZI-Project/ozi-core/commit/ae1a78e1ef385b5372f2277633d1a145685bba89))

* build(deps): bump OZI-Project/draft from 1.0.2 to 1.1.0

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 1.0.2 to 1.1.0.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/1.0.2...1.1.0)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`73b379f`](https://github.com/OZI-Project/ozi-core/commit/73b379f795806c415964043c61048da774d2b11d))

* build(deps): bump OZI-Project/publish from 1.0.2 to 1.1.0

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.0.2 to 1.1.0.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.0.2...1.1.0)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`3f17126`](https://github.com/OZI-Project/ozi-core/commit/3f17126874c680222dccb15388eb5845655b8cc6))


### Performance improvements


* perf: run lint — rjdbcm <rjdbcm@outlook.com>
([`6ecc276`](https://github.com/OZI-Project/ozi-core/commit/6ecc276a5405e7bb31614c9d142801060a748b3c))

* perf: finish i18n for CLI — rjdbcm <rjdbcm@outlook.com>
([`fe74ffc`](https://github.com/OZI-Project/ozi-core/commit/fe74ffcceb3fd3f627754b8b6178e629e6da58eb))

* perf: internationalize the ``ozi-fix`` interface and ``ozi-new`` validator error messages — rjdbcm <rjdbcm@outlook.com>
([`5eff10a`](https://github.com/OZI-Project/ozi-core/commit/5eff10ac440b2e95d325f0d08d809824dbf2b85f))

* perf: complete internationalization of ``ozi-new`` CLI — rjdbcm <rjdbcm@outlook.com>
([`182839b`](https://github.com/OZI-Project/ozi-core/commit/182839b5665ee21ffbbbc8a21bb26c0e4c2203aa))

* perf: add a License-File prompt and validator — rjdbcm <rjdbcm@outlook.com>
([`976f02e`](https://github.com/OZI-Project/ozi-core/commit/976f02e9f468af8f7190c311f18623519c2eaad9))

## 1.2.4 (2024-10-02)


### Bug fixes


* fix: typos in i18n — rjdbcm <rjdbcm@outlook.com>
([`4927181`](https://github.com/OZI-Project/ozi-core/commit/492718139b3ace0a8ebe360e6b813185bb35d044))


### Build system


* build(deps): bump OZI-Project/release from 1.0.0 to 1.0.1

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 1.0.0 to 1.0.1.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/98248899bb8b235e3198105f080093ea5b9751d8...3015ae773cba4b74f1ff7afb55ad1e6324d56f51)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`a882caa`](https://github.com/OZI-Project/ozi-core/commit/a882caab8127afb2cbd057337a5188e107d6880e))

* build(deps): bump OZI-Project/checkpoint from 1.0.0 to 1.0.1

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 1.0.0 to 1.0.1.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/1.0.0...1.0.1)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`027e98b`](https://github.com/OZI-Project/ozi-core/commit/027e98b58c3fa2d7cf90fb902b9aa5807b20e25a))

* build(deps): bump OZI-Project/publish from 1.0.0 to 1.0.2

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 1.0.0 to 1.0.2.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/1.0.0...1.0.2)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`6f90e4f`](https://github.com/OZI-Project/ozi-core/commit/6f90e4fda98a13f35f5df8a53ed6c80f78e6a2d0))

* build(deps): bump OZI-Project/draft from 1.0.0 to 1.0.2

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 1.0.0 to 1.0.2.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/1.0.0...1.0.2)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`a774a0e`](https://github.com/OZI-Project/ozi-core/commit/a774a0ea6c8813de5852e5a88d4c7771cca84e56))

## 1.2.3 (2024-10-01)


### Bug fixes


* fix(coverage): no cover — rjdbcm <rjdbcm@outlook.com>
([`7fb3df0`](https://github.com/OZI-Project/ozi-core/commit/7fb3df0e049c905a1fa9a94e7f26436eca741b0d))

* fix(i18n): patch some missing translations — rjdbcm <rjdbcm@outlook.com>
([`5383a6f`](https://github.com/OZI-Project/ozi-core/commit/5383a6fc645e1bf9c8bec13a7c00054c5bb20f70))

## 1.2.2 (2024-10-01)


### Bug fixes


* fix: correct locale file location — rjdbcm <rjdbcm@outlook.com>
([`392d0ab`](https://github.com/OZI-Project/ozi-core/commit/392d0ab8a3d19fa0367672b799ad12078c5c6437))

## 1.2.1 (2024-10-01)


### Bug fixes


* fix(i18n): fix typechecking for Python 3.10 — rjdbcm <rjdbcm@outlook.com>
([`8d2a844`](https://github.com/OZI-Project/ozi-core/commit/8d2a844be7a0b16bd07482f2f4cc7bb3198cfcba))


### Performance improvements


* perf(mypy): type locale as str — rjdbcm <rjdbcm@outlook.com>
([`b416fc0`](https://github.com/OZI-Project/ozi-core/commit/b416fc02eaa6c5654e81544de5021615f0aedf17))

* perf: update OZI wrapfile to 1.22 — rjdbcm <rjdbcm@outlook.com>
([`8e20899`](https://github.com/OZI-Project/ozi-core/commit/8e20899ddf07d5a4085779699939188abfae41fb))

## 1.2.0 (2024-09-18)


### Features


* feat: OZI 1.22 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`6f4c7b5`](https://github.com/OZI-Project/ozi-core/commit/6f4c7b50ec756e613f2e7ed5ab6fd4227ad10517))

## 1.1.1 (2024-09-11)


### Bug fixes


* fix: package metadata download-url correction — rjdbcm <rjdbcm@outlook.com>
([`08a20ee`](https://github.com/OZI-Project/ozi-core/commit/08a20eedf26623035e15f900742a156aa1d32b18))


### Build system


* build(deps): update ozi-templates requirement from ~=2.11.1 to ~=2.12.0

Updates the requirements on [ozi-templates](https://github.com/OZI-Project/ozi-templates) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-templates/releases)
- [Changelog](https://github.com/OZI-Project/ozi-templates/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-templates/compare/2.11.1...2.12.0)


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`5d57ccc`](https://github.com/OZI-Project/ozi-core/commit/5d57ccc446f36773b6f1588c280d5add8214f7f3))

* build(deps): bump step-security/harden-runner from 2.9.1 to 2.10.1

Bumps [step-security/harden-runner](https://github.com/step-security/harden-runner) from 2.9.1 to 2.10.1.
- [Release notes](https://github.com/step-security/harden-runner/releases)
- [Commits](https://github.com/step-security/harden-runner/compare/5c7944e73c4c2a096b17a9cb74d65b6c2bbafbde...91182cccc01eb5e619899d80e4e971d6181294a7)


updated-dependencies:
- dependency-name: step-security/harden-runner
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`c624d07`](https://github.com/OZI-Project/ozi-core/commit/c624d07abc4c6d83010e75ce5dafc91420ec807c))

* build(deps): update ozi-spec requirement from ~=0.9.5 to ~=0.10.0

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.9.5...0.10.0)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`04c7765`](https://github.com/OZI-Project/ozi-core/commit/04c776564057f68b81a0fbf0aec642f4cfa366af))


### Features


* feat: Merge pull request #162 from OZI-Project/dependabot/pip/ozi-templates-approx-eq-2.12.0

build(deps): update ozi-templates requirement from ~=2.11.1 to ~=2.12.0
([`efc5cb6`](https://github.com/OZI-Project/ozi-core/commit/efc5cb656ea0de930ebd2671fb493b8adab8156b))


### Performance improvements


* perf(i18n): interactive prompt and added Chinese (simplified) language support — rjdbcm <rjdbcm@outlook.com>
([`9c63941`](https://github.com/OZI-Project/ozi-core/commit/9c63941044724e49cf73e287a773a1a2b31bd3ca))


### Unknown


* :construction_worker: clean up some ``no cover`` — rjdbcm <rjdbcm@outlook.com>
([`d73e3a2`](https://github.com/OZI-Project/ozi-core/commit/d73e3a2250def23409a53aabcc2d0edc916e179e))

## 1.1.0 (2024-09-10)


### Build system


* build(deps): bump OZI-Project/checkpoint from 0.5.2 to 1.0.0

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 0.5.2 to 1.0.0.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/0.5.2...1.0.0)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-major
... — dependabot[bot] <support@github.com>
([`0dfd86e`](https://github.com/OZI-Project/ozi-core/commit/0dfd86ebddb2e456b5d5d380dd4882620971fdaa))

* build(deps): bump OZI-Project/publish from 0.1.11 to 1.0.0

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 0.1.11 to 1.0.0.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/0.1.11...1.0.0)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-major
... — dependabot[bot] <support@github.com>
([`b9becab`](https://github.com/OZI-Project/ozi-core/commit/b9becabfc8678be97a4850208b8b800e47e2f116))

* build(deps): bump OZI-Project/draft from 0.3.11 to 1.0.0

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.11 to 1.0.0.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.11...1.0.0)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-major
... — dependabot[bot] <support@github.com>
([`5c3d430`](https://github.com/OZI-Project/ozi-core/commit/5c3d430ba533a15b5a1aaffe55c495ff7af92be0))

* build(deps): bump OZI-Project/release from 0.8.11 to 1.0.0

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.8.11 to 1.0.0.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/4277e29de16b07dac4a89c8f7970c2da65554d17...98248899bb8b235e3198105f080093ea5b9751d8)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-major
... — dependabot[bot] <support@github.com>
([`25a7b48`](https://github.com/OZI-Project/ozi-core/commit/25a7b4826c39be079483c158a1ded00cb4583fa3))

* build(deps): update ozi-templates requirement from ~=2.10.1 to ~=2.11.1

Updates the requirements on [ozi-templates](https://github.com/OZI-Project/ozi-templates) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-templates/releases)
- [Changelog](https://github.com/OZI-Project/ozi-templates/blob/2.11.1/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-templates/compare/2.10.1...2.11.1)


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`8d7c41e`](https://github.com/OZI-Project/ozi-core/commit/8d7c41e05f1c082ee46d6475cb629a5c6e323a7d))


### Features


* feat: CPython 3.13 support — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e472a59`](https://github.com/OZI-Project/ozi-core/commit/e472a59ce19cede7f47f9cd4204c4346970395cb))


### Unknown


* Update pyproject.toml — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e6fb90d`](https://github.com/OZI-Project/ozi-core/commit/e6fb90dbd92ffc0e023afa83640049636d311796))

## 1.0.12 (2024-09-06)


### Bug fixes


* fix: ozi-spec 0.9.4 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e575dc3`](https://github.com/OZI-Project/ozi-core/commit/e575dc3992e9a54dc37f539516bd0bcb0242a862))


### Build system


* build(deps): bump OZI-Project/release from 0.8.10 to 0.8.11

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.8.10 to 0.8.11.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/7edb07c74e124270a29b2cd5d32ce7c9fdfc0b22...4277e29de16b07dac4a89c8f7970c2da65554d17)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`2398784`](https://github.com/OZI-Project/ozi-core/commit/2398784d9e0a3c09e69f536b48aa8d7f22489246))

* build(deps): bump OZI-Project/draft from 0.3.10 to 0.3.11

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.10 to 0.3.11.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.10...0.3.11)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`3dc7318`](https://github.com/OZI-Project/ozi-core/commit/3dc73182cd7161c6f99e419e12f91abd95eba467))

* build(pyproject.toml): remove dev dependency group — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e8e26e8`](https://github.com/OZI-Project/ozi-core/commit/e8e26e84d97f63e59fe3c26a0370bff6b98d2fda))

* build(deps): bump OZI-Project/draft from 0.3.9 to 0.3.10

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.9 to 0.3.10.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.9...0.3.10)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`d2e9b24`](https://github.com/OZI-Project/ozi-core/commit/d2e9b24da8402e4d7c260e7779c26d35885a661b))

* build(deps): bump OZI-Project/publish from 0.1.10 to 0.1.11

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 0.1.10 to 0.1.11.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/0.1.10...0.1.11)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`5722ecc`](https://github.com/OZI-Project/ozi-core/commit/5722ecc8a5f4257d4c56d83a91e3d22c2cfb6086))


### Unknown


* Update dependabot.yml — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`2316fae`](https://github.com/OZI-Project/ozi-core/commit/2316fae4ac8a26a878328f323eee91d21fb83cfb))

## 1.0.11 (2024-09-03)


### Bug fixes


* fix: ozi-spec 0.9.3 — rjdbcm <rjdbcm@outlook.com>
([`e081118`](https://github.com/OZI-Project/ozi-core/commit/e081118d62d363d864bc31a31dd9189081a1c29d))

## 1.0.10 (2024-08-31)


### Bug fixes


* fix: create README symlink with absolute path — rjdbcm <rjdbcm@outlook.com>
([`6ca9215`](https://github.com/OZI-Project/ozi-core/commit/6ca92159c3214ae094d8daf335d47d745f6f22cb))

## 1.0.9 (2024-08-31)


### Bug fixes


* fix(ozi-fix missing): no longer check if a readme file is a symlink to detect content type — rjdbcm <rjdbcm@outlook.com>
([`7a2f052`](https://github.com/OZI-Project/ozi-core/commit/7a2f0523f2d1cb25279897db7ca46b132513faa2))

## 1.0.8 (2024-08-30)

## 1.0.7 (2024-08-30)


### Build system


* build(deps): ozi-spec~=0.9.2 — rjdbcm <rjdbcm@outlook.com>
([`94645e9`](https://github.com/OZI-Project/ozi-core/commit/94645e9b591be8315311ba89454137be1e407352))


### Performance improvements


* perf: remove type key from comment diagnostic output — rjdbcm <rjdbcm@outlook.com>
([`cb08068`](https://github.com/OZI-Project/ozi-core/commit/cb08068972823ec5e16163b8ae9619fb15aceabf))

* perf: cleaned up comment diagnostic output yaml — rjdbcm <rjdbcm@outlook.com>
([`09bfc32`](https://github.com/OZI-Project/ozi-core/commit/09bfc32d032a6b2ab1f9db1670e91fc22fad6479))

## 1.0.6 (2024-08-30)

## 1.0.5 (2024-08-30)


### Bug fixes


* fix(ozi-fix missing): rendering — rjdbcm <rjdbcm@outlook.com>
([`32e95a1`](https://github.com/OZI-Project/ozi-core/commit/32e95a1b3556c88304301011251fb4cbe43997fa))

## 1.0.4 (2024-08-30)


### Bug fixes


* fix(ozi-fix missing): README content type detection, core metadata — rjdbcm <rjdbcm@outlook.com>
([`fa8716d`](https://github.com/OZI-Project/ozi-core/commit/fa8716d83972bcc1d6e003d12612f9acd51780e6))

## 1.0.3 (2024-08-30)


### Bug fixes


* fix: README text renders — rjdbcm <rjdbcm@outlook.com>
([`60ca2f0`](https://github.com/OZI-Project/ozi-core/commit/60ca2f067ec1db949f288bda10f45531ef77f3f8))

## 1.0.2 (2024-08-30)


### Bug fixes


* fix(ozi-fix missing): classifiers now render properly — rjdbcm <rjdbcm@outlook.com>
([`c004a10`](https://github.com/OZI-Project/ozi-core/commit/c004a1014e8544fc2c8e5e50d427613afb324401))

## 1.0.1 (2024-08-30)


### Bug fixes


* fix: render METADATA for ``ozi-fix missing`` — rjdbcm <rjdbcm@outlook.com>
([`932a611`](https://github.com/OZI-Project/ozi-core/commit/932a6117416c3837b49560f9e97209f80980a473))

* fix: missing parses OZI 1.20 style dependencies — rjdbcm <rjdbcm@outlook.com>
([`55a3941`](https://github.com/OZI-Project/ozi-core/commit/55a3941cfc26cb39358e133ed5f836a989ea3ab8))


### Performance improvements


* perf: fix shadowed variable — rjdbcm <rjdbcm@outlook.com>
([`be545e5`](https://github.com/OZI-Project/ozi-core/commit/be545e5fd09b7855e5d711696470552413abc7aa))

## 1.0.0 (2024-08-29)


### Bug fixes


* fix: correct release

BREAKING CHANGE: 1.0
([`eb199c1`](https://github.com/OZI-Project/ozi-core/commit/eb199c1e98e6d38363b51e4b8a86b866eb6e2a42))

## 0.4.0 (2024-08-29)


### Bug fixes


* fix: Update pyproject.toml tox requirements install — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`c79cac8`](https://github.com/OZI-Project/ozi-core/commit/c79cac8aedd88ad0a97c9cc179743b93503de8de))

* fix: remove requirements — rjdbcm <rjdbcm@outlook.com>
([`7835209`](https://github.com/OZI-Project/ozi-core/commit/7835209bcf5c09c7171a2b5a531fcedf3fbb4f00))

* fix: remove requires-python key — rjdbcm <rjdbcm@outlook.com>
([`63aed2c`](https://github.com/OZI-Project/ozi-core/commit/63aed2c8808e936865cf24e8a3b063975041db88))

* fix: update wrapfile — rjdbcm <rjdbcm@outlook.com>
([`8470c88`](https://github.com/OZI-Project/ozi-core/commit/8470c885dd7a6aafa4e377c88f187b1b346fa8de))


### Build system


* build(deps): ozi-templates~=2.10.1 — rjdbcm <rjdbcm@outlook.com>
([`8d3db61`](https://github.com/OZI-Project/ozi-core/commit/8d3db61216deab6dd623a03ebeda754744474af2))

* build(deps): update ozi-spec requirement from ~=0.8.1 to ~=0.9.1

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/0.9.1/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.8.1...0.9.1)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`d570726`](https://github.com/OZI-Project/ozi-core/commit/d57072676e1f2ec2e995c3421183084208c9bffa))

* build(deps): update ozi-templates requirement from ~=2.9.3 to ~=2.10.0


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`a9548da`](https://github.com/OZI-Project/ozi-core/commit/a9548da914b3cef22eb5d1bea35aacead1ed61ea))


### Features


* feat: OZI.build 1.3 ozi-templates 2.10 ozi-spec 0.9 — rjdbcm <rjdbcm@outlook.com>
([`df99c91`](https://github.com/OZI-Project/ozi-core/commit/df99c9126bbf522e47a15cf4d6d96090390ab861))


### Performance improvements


* perf: add ``# pragma: no cover`` to previously masked untested code — rjdbcm <rjdbcm@outlook.com>
([`024c204`](https://github.com/OZI-Project/ozi-core/commit/024c2041f0c176088b76662b255cd782d99d1f80))

* perf: use main revision of OZI pre-1.20 — rjdbcm <rjdbcm@outlook.com>
([`6d81567`](https://github.com/OZI-Project/ozi-core/commit/6d81567553c83234e27e658e8b4b97955273e1a8))

* perf: add install_dependencies postconf script — rjdbcm <rjdbcm@outlook.com>
([`1c594c4`](https://github.com/OZI-Project/ozi-core/commit/1c594c450a732b3492aeff6762a05b135ffb4356))


### Unknown


* Update meson.build

BREAKING: 1.0 removes requirements.in — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`b06b8f2`](https://github.com/OZI-Project/ozi-core/commit/b06b8f2a1885b949bc9c11530c43679658c13eff))

* Update README

BREAKING: 1.0 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`41ddc46`](https://github.com/OZI-Project/ozi-core/commit/41ddc467c5d5cf20c2e96cc314094055b1ba38d7))

* :bug: remove requires-python key — rjdbcm <rjdbcm@outlook.com>
([`ef37bfa`](https://github.com/OZI-Project/ozi-core/commit/ef37bfa72bbc9747850f548bb307944a1ad6e66e))

## 0.3.1 (2024-08-23)


### Build system


* build(deps): update ozi-templates requirement from ~=2.9.0 to ~=2.9.3


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`447823d`](https://github.com/OZI-Project/ozi-core/commit/447823da26b12b16de453e9b1609943bf925d69f))

* build(deps): update ozi-spec requirement from ~=0.8.0 to ~=0.8.1

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.8.0...0.8.1)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`f73eed2`](https://github.com/OZI-Project/ozi-core/commit/f73eed23b0f1e28a58fc8bdf0407cfa9acf4ebb9))

## 0.3.0 (2024-08-23)


### Build system


* build(pyproject.toml): asyncio_default_fixture_loop_scope = "function" — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`6ff7990`](https://github.com/OZI-Project/ozi-core/commit/6ff7990bff16e7c3c73556951eae1c8c8e68cd42))

* build(deps): bump OZI-Project/checkpoint from 0.5.1 to 0.5.2

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 0.5.1 to 0.5.2.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/0.5.1...0.5.2)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`6a591dc`](https://github.com/OZI-Project/ozi-core/commit/6a591dc4dae5a62558034bf5e802fbe1fd8a8b52))

* build(deps): bump OZI-Project/draft from 0.3.8 to 0.3.9

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.8 to 0.3.9.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.8...0.3.9)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`05a64a2`](https://github.com/OZI-Project/ozi-core/commit/05a64a27b40dd4f23eade8a44a38d0281cde344a))

* build(deps): bump OZI-Project/release from 0.8.9 to 0.8.10

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.8.9 to 0.8.10.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/f4172eb60419c98b5cf18c89d78cde8b553f5d15...7edb07c74e124270a29b2cd5d32ce7c9fdfc0b22)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`f075e90`](https://github.com/OZI-Project/ozi-core/commit/f075e90baa283e316caa33942888577d60fe188f))

* build(deps): bump OZI-Project/publish from 0.1.9 to 0.1.10

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 0.1.9 to 0.1.10.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/0.1.9...0.1.10)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`18068af`](https://github.com/OZI-Project/ozi-core/commit/18068af36cd2b5a396e1b30ca8084edc750497a3))

* build(deps): update ozi-spec requirement from ~=0.6.1 to ~=0.8.0

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.6.1...0.8.0)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`4e0495b`](https://github.com/OZI-Project/ozi-core/commit/4e0495b87a1572f570ee7cdb93a7fe0fe358cf18))

* build(deps): update spdx-license-list requirement from ~=3.24 to ~=3.25

Updates the requirements on [spdx-license-list](https://github.com/JJMC89/spdx-license-list) to permit the latest version.
- [Release notes](https://github.com/JJMC89/spdx-license-list/releases)
- [Commits](https://github.com/JJMC89/spdx-license-list/compare/v3.24.0...v3.25.0)


updated-dependencies:
- dependency-name: spdx-license-list
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`073a707`](https://github.com/OZI-Project/ozi-core/commit/073a707fd7a89f8150f004d724cf3b2e27170d3f))


### Features


* feat(deps): ozi-templates~=2.9.0 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`54d06b7`](https://github.com/OZI-Project/ozi-core/commit/54d06b79482a85a25ba6e1cf9ff7ff5872c07edf))

* feat(deps): ozi-templates~=2.9.0 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`db49f4e`](https://github.com/OZI-Project/ozi-core/commit/db49f4e3b1bb3ebf8b260d70cbe0cac121dd37f0))

* feat(deps): ozi-templates~=2.9.0 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e4150c1`](https://github.com/OZI-Project/ozi-core/commit/e4150c18273f41a599f06a8aad0a692f26271fe5))

## 0.2.4 (2024-08-18)


### Bug fixes


* fix: hide TAP version output during rewriter — rjdbcm <rjdbcm@outlook.com>
([`8c654e4`](https://github.com/OZI-Project/ozi-core/commit/8c654e4f94691028961dfbdc33c52bc28c55fd03))

* fix(ozi-new interactive): enable uv working — rjdbcm <rjdbcm@outlook.com>
([`8bd82b5`](https://github.com/OZI-Project/ozi-core/commit/8bd82b53ffa5bbf5ccffad8594c78d530e93cae2))


### Performance improvements


* perf: move jinja2 import to typechecking block — rjdbcm <rjdbcm@outlook.com>
([`72fef5d`](https://github.com/OZI-Project/ozi-core/commit/72fef5d5f882b41eb0a3a0909cff2edf4dec30d0))

## 0.2.3 (2024-08-18)


### Build system


* build(pyproject.toml): add uv dep — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`6bf4566`](https://github.com/OZI-Project/ozi-core/commit/6bf4566fc6595b1061ed6d03638f347e5f3016d2))


### Unknown


* :pushpin: ozi-templates~=2.8.2 — rjdbcm <rjdbcm@outlook.com>
([`bf7c319`](https://github.com/OZI-Project/ozi-core/commit/bf7c31958817b1ef8761d480e53c6e4e65eb0ce0))

## 0.2.2 (2024-08-16)


### Performance improvements


* perf: add ``--enable-uv`` argument expected in OZI spec 0.6 — rjdbcm <rjdbcm@outlook.com>
([`a2fdd6b`](https://github.com/OZI-Project/ozi-core/commit/a2fdd6bbc4c6225ca90ee1851d4e5c1180ae7272))

## 0.2.1 (2024-08-16)


### Build system


* build(deps): update ozi-spec requirement from ~=0.5.10 to ~=0.6.1

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.5.10...0.6.1)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`7e69af3`](https://github.com/OZI-Project/ozi-core/commit/7e69af3d275247695b1d2bb0ab6984c002ea6fdc))

* build(deps): update ozi-templates requirement from ~=2.7.1 to ~=2.8.0


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`137af6b`](https://github.com/OZI-Project/ozi-core/commit/137af6b59d728f5f462b82073f75e05b887ae015))

## 0.2.0 (2024-08-15)


### Features


* feat: OZI-Templates 2.7

GitHub workflows are no longer hardened by default.
Wheels are now built with release 0.8 which can build extension wheels! — rjdbcm <rjdbcm@outlook.com>
([`607b555`](https://github.com/OZI-Project/ozi-core/commit/607b555d1c638551853ef7b6372bdff919769f4d))


### Unknown


* :rotating_light: run black — rjdbcm <rjdbcm@outlook.com>
([`bfe1b1b`](https://github.com/OZI-Project/ozi-core/commit/bfe1b1bf43c6dedf9b87ca74fe53b804e7f6ab34))

## 0.1.21 (2024-08-12)


### Performance improvements


* perf: TAP-Producer~=1.0.4 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`9ab7475`](https://github.com/OZI-Project/ozi-core/commit/9ab7475350b47e96de48efa7ccb40dd5a6fd3721))

## 0.1.20 (2024-08-12)


### Bug fixes


* fix: OZI-Project/release@0.8.9 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`24a04fc`](https://github.com/OZI-Project/ozi-core/commit/24a04fc6443fc65cae87513faf49907ae42ea276))

* fix: update release workflow — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`2be9889`](https://github.com/OZI-Project/ozi-core/commit/2be98899a9c31cd141fbe2b4d18782c0ce8f0caa))


### Build system


* build(deps): bump OZI-Project/release from 0.8.5 to 0.8.7

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.8.5 to 0.8.7.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/0.8.5...0.8.7)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`8575198`](https://github.com/OZI-Project/ozi-core/commit/85751987f1493d01d43106563162a575bedb473d))

* build(deps): update ozi-templates requirement from ~=2.6.1 to ~=2.6.4


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`d3d5cb0`](https://github.com/OZI-Project/ozi-core/commit/d3d5cb05694abf0d50833b89781558579a92cc4d))

## 0.1.19 (2024-08-12)


### Bug fixes


* fix: patch trigger — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`f175b58`](https://github.com/OZI-Project/ozi-core/commit/f175b58256581e6c8dd3f061eb4fecb7162833db))


### Performance improvements


* perf: run lint
([`7bf2d0a`](https://github.com/OZI-Project/ozi-core/commit/7bf2d0abac0288f193c6dff1877d7caab02172df))


### Unknown


* :children_crossing: clean up diagnostic outputs — rjdbcm <rjdbcm@outlook.com>
([`e2ae6bd`](https://github.com/OZI-Project/ozi-core/commit/e2ae6bdbadf9fa38c61bcd101dbf0e7f7240bfa3))

## 0.1.18 (2024-08-11)


### Bug fixes


* fix(ozi-new): set TAP.version before parsing args — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`4ce1d1c`](https://github.com/OZI-Project/ozi-core/commit/4ce1d1c055ac3b5c4ac852382325ae73453ac834))


### Build system


* build: update ozi.yml allowed endpoints — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`3ee473d`](https://github.com/OZI-Project/ozi-core/commit/3ee473d61f7fc6c8246af013b5b7693d5b736587))

* build(deps): bump OZI-Project/release from 0.7.4 to 0.8.5

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.7.4 to 0.8.5.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/0.7.4...0.8.5)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`d78bc4a`](https://github.com/OZI-Project/ozi-core/commit/d78bc4ab30aebaad18cca25531c7f1fe300100c4))

## 0.1.17 (2024-08-07)


### Build system


* build(deps): update ozi-templates requirement from ~=2.5.8 to ~=2.6.1


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`87a7da5`](https://github.com/OZI-Project/ozi-core/commit/87a7da50ea70f596e277469538dfb73113a1f4ef))

## 0.1.16 (2024-08-07)


### Build system


* build(deps): update tap-producer requirement from ~=0.2 to ~=1.0

Updates the requirements on [tap-producer](https://github.com/OZI-Project/TAP-Producer) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/TAP-Producer/releases)
- [Changelog](https://github.com/OZI-Project/TAP-Producer/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/TAP-Producer/compare/0.2.0...1.0.0)


updated-dependencies:
- dependency-name: tap-producer
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`f122071`](https://github.com/OZI-Project/ozi-core/commit/f1220712a2763fde9d562fee76cd4eebdd7dcd87))

* build(deps): update ozi-spec requirement from ~=0.5.8 to ~=0.5.9

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/0.5.9/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.5.8...0.5.9)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`caae3de`](https://github.com/OZI-Project/ozi-core/commit/caae3de352cd02488393e5a88aeee45a1c824137))

* build(deps): bump OZI-Project/checkpoint from 0.5.0 to 0.5.1

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 0.5.0 to 0.5.1.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/0.5.0...0.5.1)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`2b5c025`](https://github.com/OZI-Project/ozi-core/commit/2b5c02551ff2e40ad6fd48cb998819c0513b66dd))

* build(deps): bump OZI-Project/release from 0.7.3 to 0.7.4

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.7.3 to 0.7.4.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/0.7.3...0.7.4)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`9a2de2f`](https://github.com/OZI-Project/ozi-core/commit/9a2de2f6274362809ac0c63f2c472f44eeec867d))

* build(deps): bump step-security/harden-runner from 2.9.0 to 2.9.1

Bumps [step-security/harden-runner](https://github.com/step-security/harden-runner) from 2.9.0 to 2.9.1.
- [Release notes](https://github.com/step-security/harden-runner/releases)
- [Commits](https://github.com/step-security/harden-runner/compare/0d381219ddf674d61a7572ddd19d7941e271515c...5c7944e73c4c2a096b17a9cb74d65b6c2bbafbde)


updated-dependencies:
- dependency-name: step-security/harden-runner
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`3365971`](https://github.com/OZI-Project/ozi-core/commit/3365971d93c97a895be9478e958729bed73378dc))

* build(deps): bump OZI-Project/draft from 0.3.7 to 0.3.8

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.7 to 0.3.8.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.7...0.3.8)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`04aa4b1`](https://github.com/OZI-Project/ozi-core/commit/04aa4b15977ebc84bd6a98bbee98e42dd1f4594a))

* build: Update pyproject.toml:tool.semantic_release.commit_parser_options.patch_tags add build — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`553efa8`](https://github.com/OZI-Project/ozi-core/commit/553efa89fb9426e101a65d6a32d9fc39a48d15d8))

* build(deps): update ozi-templates requirement from ~=2.5.6 to ~=2.5.8


updated-dependencies:
- dependency-name: ozi-templates
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`d937739`](https://github.com/OZI-Project/ozi-core/commit/d9377391f26d9a2234b16d6fc9895c2fdb29cccc))


### Performance improvements


* perf: refactor interactive submodule — rjdbcm <rjdbcm@outlook.com>
([`1d13d8e`](https://github.com/OZI-Project/ozi-core/commit/1d13d8e594ce2121f811462bed5bc4d05e7757ad))

## 0.1.15 (2024-07-30)


### Build system


* build(deps): update ozi-spec requirement from ~=0.5.7 to ~=0.5.8

Updates the requirements on [ozi-spec](https://github.com/OZI-Project/ozi-spec) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/ozi-spec/releases)
- [Changelog](https://github.com/OZI-Project/ozi-spec/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/ozi-spec/compare/0.5.7...0.5.8)


updated-dependencies:
- dependency-name: ozi-spec
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`87a9703`](https://github.com/OZI-Project/ozi-core/commit/87a970368906f23468e0dce658f3b95d9fe4856d))


### Performance improvements


* perf: Merge pull request #50 from OZI-Project/main

Release
([`7286ba3`](https://github.com/OZI-Project/ozi-core/commit/7286ba3a407aee2821624f78a8e45793c7147f58))

## 0.1.14 (2024-07-29)


### Performance improvements


* perf: TAP-Producer~=0.2 — rjdbcm <rjdbcm@outlook.com>
([`806e4e6`](https://github.com/OZI-Project/ozi-core/commit/806e4e690f036834aa5f2d79c9b2eb6c027f0462))

* perf: ozi-spec~=0.5.7 — rjdbcm <rjdbcm@outlook.com>
([`25905f1`](https://github.com/OZI-Project/ozi-core/commit/25905f119deb214f69ece76753f56386f6715e77))

* perf: use TAP version 14 in ``ozi-new`` and ``ozi-fix`` — rjdbcm <rjdbcm@outlook.com>
([`4e65ef5`](https://github.com/OZI-Project/ozi-core/commit/4e65ef546af4472125add85e2a4f987a38813526))

## 0.1.13 (2024-07-28)


### Bug fixes


* fix: gitpython~=3.1 — rjdbcm <rjdbcm@outlook.com>
([`fd822c6`](https://github.com/OZI-Project/ozi-core/commit/fd822c640c0b469e71d46ea7f279a8b5cb42ae88))

## 0.1.12 (2024-07-25)


### Bug fixes


* fix(requirements.in): ozi-spec~=0.5.7 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`2aa4a87`](https://github.com/OZI-Project/ozi-core/commit/2aa4a87cedecb07bf0e68f0f19b9131269ddf2e7))

## 0.1.11 (2024-07-25)


### Build system


* build(deps): bump OZI-Project/publish from 0.1.8 to 0.1.9

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 0.1.8 to 0.1.9.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/0.1.8...0.1.9)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`452ad21`](https://github.com/OZI-Project/ozi-core/commit/452ad214b47668d8dd6112a2e51d1029b32624a6))

* build(deps): bump OZI-Project/draft from 0.3.6 to 0.3.7

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.6 to 0.3.7.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.6...0.3.7)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`905c8dd`](https://github.com/OZI-Project/ozi-core/commit/905c8ddb2294e12d17db0ff8c8763c15746e6f5f))

## 0.1.10 (2024-07-22)


### Build system


* build(deps): update tap-producer requirement from ~=0.1.4 to ~=0.2.0

Updates the requirements on [tap-producer](https://github.com/OZI-Project/TAP-Producer) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/TAP-Producer/releases)
- [Changelog](https://github.com/OZI-Project/TAP-Producer/blob/main/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/TAP-Producer/compare/0.1.4...0.2.0)


updated-dependencies:
- dependency-name: tap-producer
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`31f6262`](https://github.com/OZI-Project/ozi-core/commit/31f626294d42088b072aa00704c14af2a4d06d39))

## 0.1.9 (2024-07-19)

## 0.1.8 (2024-07-19)

## 0.1.7 (2024-07-19)


### Bug fixes


* fix: use ``ozi.version`` as key for wrapfile release revision selection — rjdbcm <rjdbcm@outlook.com>
([`708552c`](https://github.com/OZI-Project/ozi-core/commit/708552cf3928b49393f8443c11659e8db71ba093))

* fix: move remaining core functionality to package — rjdbcm <rjdbcm@outlook.com>
([`0bb22a3`](https://github.com/OZI-Project/ozi-core/commit/0bb22a3efa9022386155a8cf3626e89429552a3a))

* fix: ozi-core~=0.5.6 — rjdbcm <rjdbcm@outlook.com>
([`485227f`](https://github.com/OZI-Project/ozi-core/commit/485227fc49d271ff8d946fc3cff33c4555c40f8e))

* fix: correct changelog title — rjdbcm <rjdbcm@outlook.com>
([`a01e5ce`](https://github.com/OZI-Project/ozi-core/commit/a01e5ceb1f51e084ceb4bc49bd15f08de8dd450c))

* fix: correct ``templates/templates/*`` names to include ``.j2`` extension — rjdbcm <rjdbcm@outlook.com>
([`ba9a68d`](https://github.com/OZI-Project/ozi-core/commit/ba9a68d5bfaba9513af8480fcc604527211de017))

* fix: ozi-spec~=0.5.5

Implements sigstore-v3 workflows. — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`a2b2eac`](https://github.com/OZI-Project/ozi-core/commit/a2b2eacb4113d711077724c8b9ceced4071ac6f6))

* fix: ozi-spec~=0.5.4 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`dc31546`](https://github.com/OZI-Project/ozi-core/commit/dc31546e5e1714f823535edceb8ee70ba6cbb60e))


### Build system


* build(deps): bump step-security/harden-runner from 2.8.0 to 2.9.0

Bumps [step-security/harden-runner](https://github.com/step-security/harden-runner) from 2.8.0 to 2.9.0.
- [Release notes](https://github.com/step-security/harden-runner/releases)
- [Commits](https://github.com/step-security/harden-runner/compare/v2.8.0...0d381219ddf674d61a7572ddd19d7941e271515c)


updated-dependencies:
- dependency-name: step-security/harden-runner
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`bef7e1e`](https://github.com/OZI-Project/ozi-core/commit/bef7e1e2b0fcb9656f28171f316296a2834a5c54))

* build(deps): update packaging requirement from ~=24.0 to ~=24.1

Updates the requirements on [packaging](https://github.com/pypa/packaging) to permit the latest version.
- [Release notes](https://github.com/pypa/packaging/releases)
- [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pypa/packaging/compare/24.0...24.1)


updated-dependencies:
- dependency-name: packaging
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`13daef7`](https://github.com/OZI-Project/ozi-core/commit/13daef726f2bc916734e06bfb59d9940247ac1cd))

* build(deps): bump OZI-Project/release from 0.6.5 to 0.7.3

Bumps [OZI-Project/release](https://github.com/ozi-project/release) from 0.6.5 to 0.7.3.
- [Release notes](https://github.com/ozi-project/release/releases)
- [Commits](https://github.com/ozi-project/release/compare/0.6.5...0.7.3)


updated-dependencies:
- dependency-name: OZI-Project/release
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`a82c406`](https://github.com/OZI-Project/ozi-core/commit/a82c40631ffb94899420873b0cdf6c4914e0a73d))

* build(deps): bump OZI-Project/publish from 0.1.7 to 0.1.8

Bumps [OZI-Project/publish](https://github.com/ozi-project/publish) from 0.1.7 to 0.1.8.
- [Release notes](https://github.com/ozi-project/publish/releases)
- [Commits](https://github.com/ozi-project/publish/compare/0.1.7...0.1.8)


updated-dependencies:
- dependency-name: OZI-Project/publish
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`152e647`](https://github.com/OZI-Project/ozi-core/commit/152e647612924699180b78034eceb99bad2798cf))

* build(deps): bump OZI-Project/draft from 0.3.4 to 0.3.6

Bumps [OZI-Project/draft](https://github.com/ozi-project/draft) from 0.3.4 to 0.3.6.
- [Release notes](https://github.com/ozi-project/draft/releases)
- [Commits](https://github.com/ozi-project/draft/compare/0.3.4...0.3.6)


updated-dependencies:
- dependency-name: OZI-Project/draft
  dependency-type: direct:production
  update-type: version-update:semver-patch
... — dependabot[bot] <support@github.com>
([`e60538c`](https://github.com/OZI-Project/ozi-core/commit/e60538c29ac5d1f618f259cf2d7c7629cd574759))

* build(deps): bump OZI-Project/checkpoint from 0.4.2 to 0.5.0

Bumps [OZI-Project/checkpoint](https://github.com/ozi-project/checkpoint) from 0.4.2 to 0.5.0.
- [Release notes](https://github.com/ozi-project/checkpoint/releases)
- [Commits](https://github.com/ozi-project/checkpoint/compare/0.4.2...0.5.0)


updated-dependencies:
- dependency-name: OZI-Project/checkpoint
  dependency-type: direct:production
  update-type: version-update:semver-minor
... — dependabot[bot] <support@github.com>
([`a3c014a`](https://github.com/OZI-Project/ozi-core/commit/a3c014aa8c0d41374a1ebea87892433459a0e6b3))

* build(deps): update tap-producer requirement from ~=0.1.1 to ~=0.1.4

Updates the requirements on [tap-producer](https://github.com/OZI-Project/TAP-Producer) to permit the latest version.
- [Release notes](https://github.com/OZI-Project/TAP-Producer/releases)
- [Changelog](https://github.com/OZI-Project/TAP-Producer/blob/0.1.4/CHANGELOG.md)
- [Commits](https://github.com/OZI-Project/TAP-Producer/compare/0.1.1...0.1.4)


updated-dependencies:
- dependency-name: tap-producer
  dependency-type: direct:production
... — dependabot[bot] <support@github.com>
([`aa61e25`](https://github.com/OZI-Project/ozi-core/commit/aa61e259ba90382d99881afd96ac425a2a42b47b))

* build(deps): ozi-templates~=2.5.5 — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`d867913`](https://github.com/OZI-Project/ozi-core/commit/d8679132219753a12f47e57411a221d4a95d310b))


### Performance improvements


* perf: Merge pull request #23 from OZI-Project/patch/sigstore-v3

Patch/sigstore v3
([`b63fd5b`](https://github.com/OZI-Project/ozi-core/commit/b63fd5b6de42e0f17b163f1fd9f1d3f74d20d7be))


### Unknown


* Update dependabot.yml — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`d0784c5`](https://github.com/OZI-Project/ozi-core/commit/d0784c5dfe89852a42a3ac2e04af6bce165ff536))

* Create dependabot.yml — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`e810ff4`](https://github.com/OZI-Project/ozi-core/commit/e810ff42fdec165967f31a39f9e14bbb6814c41e))

## 0.1.6 (2024-07-18)


### Bug fixes


* fix: OZI.build>=0.0.27 — rjdbcm <rjdbcm@outlook.com>
([`bc032f2`](https://github.com/OZI-Project/ozi-core/commit/bc032f214fc8cdfa51f6748b8f07461e301cf686))

## 0.1.5 (2024-07-18)


### Bug fixes


* fix: ozi-spec~=0.5.2 — rjdbcm <rjdbcm@outlook.com>
([`bf4a290`](https://github.com/OZI-Project/ozi-core/commit/bf4a2903a4b7fd9d8d42570e6a3ca69c2ece1af9))

## 0.1.4 (2024-07-12)


### Bug fixes


* fix: ozi missing parser accepts target — rjdbcm <rjdbcm@outlook.com>
([`0b6892c`](https://github.com/OZI-Project/ozi-core/commit/0b6892cbf9d8d1c174402746c419aa844e5cc3ab))


### Performance improvements


* perf: clean up imports
([`f993ee4`](https://github.com/OZI-Project/ozi-core/commit/f993ee46db3d06b8c62d3163b0d384d53f2723ca))

## 0.1.3 (2024-07-12)


### Performance improvements


* perf: run black — rjdbcm <rjdbcm@outlook.com>
([`0728216`](https://github.com/OZI-Project/ozi-core/commit/0728216e7c48e8bd30872d56911328241121ea19))

## 0.1.2 (2024-07-12)

## 0.1.1 (2024-07-11)


### Bug fixes


* fix: comment scoring is fixed
([`bdc4b60`](https://github.com/OZI-Project/ozi-core/commit/bdc4b60d2b90b01e412f1dbde12b6287b43da5cf))

* fix: fix comment line counting — rjdbcm <rjdbcm@outlook.com>
([`d2d0192`](https://github.com/OZI-Project/ozi-core/commit/d2d019276f49bddae27fc752312ed9ed144f68a7))

* fix(ozi.fix.parser): target as final argument — rjdbcm <rjdbcm@outlook.com>
([`3afe42f`](https://github.com/OZI-Project/ozi-core/commit/3afe42f3bde8113f53b8f87aeb8cc49645375051))

## 0.1.0 (2024-07-11)

## 0.0.2 (2024-07-11)

## 0.0.1 (2024-07-11)


### Bug fixes


* fix: override version arg for ``actions.info`` — rjdbcm <rjdbcm@outlook.com>
([`dcb0b8f`](https://github.com/OZI-Project/ozi-core/commit/dcb0b8f8eeb6eacf05910eb8e461c0f1114ac5fb))

* fix(ozi_core.fix.parser): target always last argument — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`52a135a`](https://github.com/OZI-Project/ozi-core/commit/52a135a3806af39bc30b5cf66461995fe6bd3af8))

* fix(ozi_core.new.parser): target now the last argument — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`92f8b86`](https://github.com/OZI-Project/ozi-core/commit/92f8b868f23778c835f522b64730819eaf48c97e))

* fix(requirements.in): add ``prompt-toolkit`` — Eden Ross Duff, MSc <rjdbcm@outlook.com>
([`f5ccb78`](https://github.com/OZI-Project/ozi-core/commit/f5ccb78f3e1f6165052b25635c85564219cc0315))


### Features


* feat: remove ``print_version`` and add version arg to ``check_version`` — rjdbcm <rjdbcm@outlook.com>
([`d88a200`](https://github.com/OZI-Project/ozi-core/commit/d88a2008163c244b56ffffdacb0727ca0d039f85))

## 0.0.0 (2024-07-10)


### Unknown


* init
([`fc288f5`](https://github.com/OZI-Project/ozi-core/commit/fc288f56d4e0f31b3e4150ec4d6829df61ac117c))



## 0.0.0 (2024-07-09)

### :tada:

* :tada:: Initialized ozi-core with ``ozi-new``.

```sh
ozi-new project --name ozi-core --summary 'The OZI Project packaging core library.' --keywords OZI,mesonbuild --home-page https://www.oziproject.dev --author 'Eden Ross Duff MSc' --author-email help@oziproject.dev --license 'OSI Approved :: Apache Software License' --license-expression 'Apache-2.0 WITH LLVM-exception' --requires-dist 'pyparsing~=3.1' --requires-dist 'GitPython>=3' --requires-dist 'TAP-Producer~=0.1.1' --requires-dist 'meson[ninja]>=1.1.0' --requires-dist requests --requires-dist types-requests --requires-dist 'packaging~=24.0' --requires-dist spdx-license-list --requires-dist 'ozi-spec~=0.5' --requires-dist 'ozi-templates~=2.5.1'
```