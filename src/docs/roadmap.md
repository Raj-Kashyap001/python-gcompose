# gcompose - Roadmap

gcompose is a **declarative UI framework built on top of GTK4 + Libadwaita**, inspired by other popular layouts.

The primary goal is: > make GTK application developement **simple and enjoyable**

## Core Principles

- Functional UI: `UI = fn(state)`
- Composables over classes
- Explicit state updates
- Native GTK widgets (no virtual DOM)
- Simple before powerful
- Features exist only when needed by examples

---

## Versioning Strategy

Each version:

- Adds the **minimum features** required
- Ships with **one example app**
- Freezes API at the end of the version

---

## v1 — Foundations (Current)

### Goal

Prove that GTK apps can be built declaratively with minimal boilerplate.

### Features

- `@Composable` functions
- Composition stack
- `use_state(initial)`
- Full UI re-render on state change
- Layout primitives with all posible styling option inspired by web:
  - `Column`
  - `Row`
- Basic widgets:
  - `Text`
  - `Button`
- Single-window app host
