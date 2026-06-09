# dbt-semantic-mcp

> DuckDB + dbt medallion marts + a governed semantic layer (MetricFlow), exposed to agents over MCP

## Why

Two paragraphs. The problem. Why existing options didn't fit. Read this
**before** asking what it does.

(Replace this placeholder with real "why" content. A reader should
understand the motivation before encountering any code.)

## What

One paragraph. What this actually is — a CLI, a library, a service, a
config bundle. Concrete enough that someone can decide in 30 seconds
whether to keep reading.

## Quickstart

```sh
git clone <url> dbt-semantic-mcp && cd dbt-semantic-mcp
just            # see all recipes
just check      # fmt + lint + test
```

## Usage

(Real usage examples go here. For libraries: a minimal "hello-world"
import-and-call snippet. For CLIs: the most useful subcommand. For
services: how to run it locally.)

## Development

```sh
pre-commit install   # one-time after clone
just                 # list recipes
just check           # the merge gate
```

See `CLAUDE.md` for engineering conventions; `docs/adr/` for design
decisions; `CONTRIBUTING.md` (Tier 2 only) for contribution guidelines.

## License

(License footer — `/new-project` substitutes the appropriate snippet
based on `apache-mit-dual`. For dual Apache-2.0 OR MIT, see
`licenses/README-license-snippet.md`.)
<!--
  Drop this snippet into the project README under a `## License` heading
  when the project is dual-licensed Apache-2.0 OR MIT (Decision 1).
  The `/new-project` skill copies this in automatically when
  --license=apache-mit-dual (the default).
-->

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or
  <http://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or
  <http://opensource.org/licenses/MIT>)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in this project by you, as defined in the
Apache-2.0 license, shall be dual licensed as above, without any
additional terms or conditions.
