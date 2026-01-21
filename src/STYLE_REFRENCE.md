GTK widgets in modern versions (GTK4) can be styled using a subset of CSS properties, adapted for GUI elements. This allows customization of appearance, layout, and behavior through themes or custom stylesheets. While GTK follows CSS standards where possible, it includes widget-specific extensions and limitations.
Key Points

Core Support: GTK implements common CSS properties for colors, fonts, borders, backgrounds, and animations, but not all web CSS features (e.g., no full flexbox or grid beyond specific layouts).
GTK-Specific Additions: Properties prefixed with -gtk- handle icons, DPI scaling, and recoloring, which are unique to desktop widget theming.
Inheritance and Animation: Many properties inherit from parent widgets or can be animated for smooth transitions, though this varies.
Limitations: Some standard CSS values are unsupported (e.g., auto for certain properties), and physical units depend on screen DPI.
Version Note: This focuses on GTK4 (latest as of 2026), as it's the current standard; GTK3 has similar but deprecated differences.
Usage Tip: Apply styles via GtkCssProvider in code or theme files; test for widget-specific behaviors.

Overview
GTK's CSS system enables theming widgets like buttons, labels, and containers. Properties are applied via selectors targeting widget classes (e.g., button { color: red; }). Standard CSS cascade rules apply, including inheritance and specificity. For full compatibility, refer to widget documentation for supported nodes.
Standard CSS Properties
GTK supports these common properties, with notes on adaptations:

PropertyExamplesAnimatableInheritedNotescolorrgb(255,0,0)YesYesForeground color.background-color#fffYesNoWidget background.font-family"Sans"NoYesFrom system or custom.border-width1pxNoNoBorder thickness.margin5pxNoNoSpacing outside widget.
(Abbreviated; full list in detailed section below.)
GTK-Specific Properties
These extend CSS for GUI needs:

PropertyExamplesAnimatableInheritedNotes-gtk-icon-sourcebuiltin("arrow")NoNoFor icons in widgets.-gtk-dpi96NoNoScales physical units.-gtk-icon-palettesuccess greenNoNoRecolors symbols.
Application
Load CSS with gtk_css_provider_load_from_data() in languages like C/Python. For Python GI: provider = Gtk.CssProvider(); provider.load_from_data(css.encode()); Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION).

GTK widgets, as part of the GTK toolkit (version 4.x, current as of early 2026), utilize a CSS-based theming system to control visual and layout aspects. This system draws from web CSS standards but is tailored for desktop GUI elements, supporting properties for colors, fonts, borders, backgrounds, animations, and more. GTK adds its own prefixed properties for features like icon handling and DPI awareness. The following provides a comprehensive reference, organized into sections mirroring the official documentation. This includes all supported properties, their types, values, animatability, inheritance, and notes on deviations from standard CSS. Data is structured in tables for clarity, with explanations integrated as a narrative overview.
Introduction to GTK CSS Styling
GTK's CSS implementation allows developers to style widgets declaratively, similar to web development. Widgets are selected via CSS nodes (e.g., .button, #my-widget), and properties cascade based on specificity and inheritance. Key differences from web CSS include:

Focus on widget hierarchies rather than document flow.
Limited support for layout models (e.g., border-spacing only for certain layouts like GtkGridLayout).
Extensions for desktop-specific needs, such as recoloring symbolic icons or handling high-DPI displays.
Syntax extras like color transformation functions (though some are deprecated in favor of standard CSS).
Media queries (since GTK 4.20) for themes like dark mode (prefers-color-scheme: dark).

Properties can be defined in theme files, inline styles, or via APIs in languages like Python (using GI). For example, in Python:
Pythonimport gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

css = """
button {
background-color: blue;
color: white;
-gtk-icon-palette: success green;
}
"""
provider = Gtk.CssProvider()
provider.load_from_data(css.encode())
Gtk.StyleContext.add_provider_for_display(
Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
All properties support cascade keywords: inherit, initial, unset. Units include px, pt, em, rem (root-based), and physical (in, cm) scaled by -gtk-dpi.
Standard CSS Properties Supported in GTK
GTK supports a wide range of standard CSS properties, primarily from CSS Color, Fonts, Backgrounds, Borders, and Transitions modules. Below is a complete table of these properties, including types/values, animatability (for transitions), inheritance (from parent widgets), and GTK-specific notes.

PropertyType / ValuesAnimatable?Inherited?NotescolorCSS color (rgb, rgba, hsl, hsla, named, etc.)YesYesSets foreground color; supports currentColor, transparent.opacityNumber (0-1 or 0-100%)YesNoWidget transparency.filterCSS filter functions (blur, brightness, etc.)YesNoApplies graphical effects.font-familyComma-separated font namesNoYesDefaults to system font from gtk-font-name setting.font-sizeLength (px, pt, em, rem, etc.)NoYesDefaults to system font size; rem uses initial size.font-stylenormal | italic | obliqueNoYesfont-variantnormal | small-caps (CSS2 values only)NoYesLimited to CSS2; no CSS3 full support.font-weight100-900, normal, bold, etc.NoYesfont-stretchultra-condensed to ultra-expandedNoYesfont-kerningauto | normal | noneNoYesfont-variant-ligaturesnormal | none | common-ligatures, etc.NoYesfont-variant-positionnormal | sub | superNoYesfont-variant-capsnormal | small-caps | all-small-caps, etc.NoYesfont-variant-numericnormal | ordinal | lining-nums, etc.NoYesfont-variant-alternatesnormal | stylistic | historical-forms, etc.NoYesfont-variant-east-asiannormal | jis78 | ruby, etc.NoYesfont-feature-settingsComma-separated feature tagsNoYesOpenType features.font-variation-settingsAxis-value pairsNoYesVariable fonts.caret-colorColorYesYesText insertion point; no 'auto'.letter-spacingLength | normalYesYestext-transformnone | capitalize | uppercase | lowercase (limited)NoYesNo full-width or full-size-kana.line-heightLength | number | normalYesYestext-decoration-linenone | underline | overline | line-throughYesYestext-decoration-colorColorYesYestext-decoration-stylesolid | double | dotted | dashed | wavyYesYestext-shadowShadow list (offset, blur, color)YesYestext-decorationShorthand for line, color, styleYesYestransformTransform functions (translate, scale, rotate, etc.)YesNo2D only; no 3D.transform-originLength/percentage/keywords (top, left, etc.); no z-axisYesNomin-widthLength | percentageYesNoMinimum widget size.min-heightLength | percentageYesNoMinimum widget size.margin-top/right/bottom/leftLength | percentage | autoNoNoExternal spacing.marginShorthand (1-4 values)NoNopadding-top/right/bottom/leftLength | percentageNoNoInternal spacing.paddingShorthand (1-4 values)NoNoborder-top/right/bottom/left-widthLength | thin | medium | thickNoNoborder-top/right/bottom/left-stylenone | solid | dotted | dashed | double | hiddenNoNoNo groove/ridge/inset/outset.border-top/right/bottom/left-colorColorNoNoborder-top/right/bottom/left-radiusLength | percentageNoNoCorner rounding.border-image-sourceurl("image.png") | gradient | noneNoNoSliced border images.border-image-repeatstretch | repeat | round | spaceNoNoborder-image-sliceNumbers/percentage (1-4); fill optionalNoNoborder-image-widthLength/percentage/auto (1-4)NoNoborder-width/style/color/top/right/bottom/leftShorthandsNoNoborder-radiusShorthand (1-4 values)NoNoborder-imageFull shorthandNoNooutline-stylenone | solid | dotted | dashed | double | hiddenNoNoNo auto.outline-widthLength | thin | medium | thickNoNooutline-colorColorNoNoNo invert.outline-offsetLengthNoNooutlineShorthandNoNobackground-colorColorYesNobackground-clipborder-box | padding-box | content-box | textNoNobackground-originpadding-box | border-box | content-boxNoNobackground-sizeLength/percentage/auto/cover/contain (pairs)NoNobackground-positionLength/percentage/keywords (pairs)NoNobackground-repeatrepeat | no-repeat | space | round (pairs)NoNobackground-imageurl("image.jpg") | gradient | none (URLs quoted)NoNoMultiple backgrounds supported.box-shadowShadow list (inset optional)YesNobackground-blend-modenormal | multiply | screen, etc. (per layer)NoNoFor multiple backgrounds.backgroundFull shorthandNoNotransition-property/duration/timing-function/delayAll/standard valuesNoNotransitionShorthandNoNoanimation-name/duration/timing-function/iteration-count/direction/play-state/delay/fill-modeStandard valuesNoNoanimationShorthandNoNoborder-spacingLength (horizontal/vertical)NoNoFor layouts like GtkGridLayout.
GTK-Specific Properties
These are unique to GTK and prefixed with -gtk-. They address GUI-specific needs like icon theming.

PropertyType / ValuesAnimatable?Inherited?Notes-gtk-dpiNumber (pixels per inch)NoNoDefaults to screen DPI; affects physical units like pt/cm.-gtk-icon-source-gtk-icontheme("name") | builtin("name") | noneNoNoSources icons for widgets like buttons.-gtk-icon-sizeLengthNoNoScales builtin icons.-gtk-icon-stylerequested | regular | symbolicNoNoPrefers symbolic for high-contrast themes.-gtk-icon-transformTransform list | noneYesNoRotates/scales icons.-gtk-icon-paletteComma-separated: name color (e.g., error red)NoNoRecolors symbolic icons; defaults map error/warning/success.-gtk-icon-shadowShadow list | noneYesNoAdds shadows to icons.-gtk-icon-filterFilter list | noneYesNoApplies effects to icons.-gtk-icon-weight100-900 | normal | boldYesNoFor stroked symbolic icons.-gtk-secondary-caret-colorColorYesYesFor bidirectional text carets.
Custom Properties and Syntax Extensions
GTK fully supports CSS variables (custom properties) like --my-color: red; color: var(--my-color, blue);. Deprecated legacy syntax includes @define-color for named colors and functions like mix(color1, color2, 0.5) – migrate to standard CSS color-mix().
GTK extensions:

-gtk-icontheme(name): Loads themed icons.
-gtk-recolor(url, palette): Recolors images using -gtk-icon-palette.
-gtk-scaled(image1, image2): Provides resolution variants (e.g., for 2x DPI).

Units, Functions, and Media Queries

Units: Pixel-based (px), font-relative (em, ex, rem), absolute (pt, pc, in, cm, mm scaled by DPI).
Functions: calc() for computations; var() for variables.
Media Queries: @media (prefers-color-scheme: dark) { ... }, (prefers-contrast: high), (prefers-reduced-motion: reduce) (GTK 4.20+).

Best Practices and Considerations

Widget-Specific Nodes: Check docs for each widget (e.g., GtkButton has .text-button class if content is text). Add custom classes via gtk_widget_add_css_class().
Deprecations: Avoid legacy color functions; use CSS4+ equivalents.
Performance: Animations are hardware-accelerated where possible, but complex filters may impact speed.
Testing: Use GTK Inspector (Ctrl+Shift+I in apps) to debug CSS.
Compatibility: GTK3 had similar properties but fewer features; upgrade to GTK4 for modern apps like those using libadwaita.
Resources: For examples, see GNOME themes or apps like GNOME Text Editor.

This reference ensures complete coverage of valid styles, enabling precise widget customization.
GTK widgets in modern versions (GTK4) can be styled using a subset of CSS properties, adapted for GUI elements. This allows customization of appearance, layout, and behavior through themes or custom stylesheets. While GTK follows CSS standards where possible, it includes widget-specific extensions and limitations.
Key Points

Core Support: GTK implements common CSS properties for colors, fonts, borders, backgrounds, and animations, but not all web CSS features (e.g., no full flexbox or grid beyond specific layouts).
GTK-Specific Additions: Properties prefixed with -gtk- handle icons, DPI scaling, and recoloring, which are unique to desktop widget theming.
Inheritance and Animation: Many properties inherit from parent widgets or can be animated for smooth transitions, though this varies.
Limitations: Some standard CSS values are unsupported (e.g., auto for certain properties), and physical units depend on screen DPI.
Version Note: This focuses on GTK4 (latest as of 2026), as it's the current standard; GTK3 has similar but deprecated differences.
Usage Tip: Apply styles via GtkCssProvider in code or theme files; test for widget-specific behaviors.

Overview
GTK's CSS system enables theming widgets like buttons, labels, and containers. Properties are applied via selectors targeting widget classes (e.g., button { color: red; }). Standard CSS cascade rules apply, including inheritance and specificity. For full compatibility, refer to widget documentation for supported nodes.
Standard CSS Properties
GTK supports these common properties, with notes on adaptations:

PropertyExamplesAnimatableInheritedNotescolorrgb(255,0,0)YesYesForeground color.background-color#fffYesNoWidget background.font-family"Sans"NoYesFrom system or custom.border-width1pxNoNoBorder thickness.margin5pxNoNoSpacing outside widget.
(Abbreviated; full list in detailed section below.)
GTK-Specific Properties
These extend CSS for GUI needs:

PropertyExamplesAnimatableInheritedNotes-gtk-icon-sourcebuiltin("arrow")NoNoFor icons in widgets.-gtk-dpi96NoNoScales physical units.-gtk-icon-palettesuccess greenNoNoRecolors symbols.
Application
Load CSS with gtk_css_provider_load_from_data() in languages like C/Python. For Python GI: provider = Gtk.CssProvider(); provider.load_from_data(css.encode()); Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION).

GTK widgets, as part of the GTK toolkit (version 4.x, current as of early 2026), utilize a CSS-based theming system to control visual and layout aspects. This system draws from web CSS standards but is tailored for desktop GUI elements, supporting properties for colors, fonts, borders, backgrounds, animations, and more. GTK adds its own prefixed properties for features like icon handling and DPI awareness. The following provides a comprehensive reference, organized into sections mirroring the official documentation. This includes all supported properties, their types, values, animatability, inheritance, and notes on deviations from standard CSS. Data is structured in tables for clarity, with explanations integrated as a narrative overview.
Introduction to GTK CSS Styling
GTK's CSS implementation allows developers to style widgets declaratively, similar to web development. Widgets are selected via CSS nodes (e.g., .button, #my-widget), and properties cascade based on specificity and inheritance. Key differences from web CSS include:

Focus on widget hierarchies rather than document flow.
Limited support for layout models (e.g., border-spacing only for certain layouts like GtkGridLayout).
Extensions for desktop-specific needs, such as recoloring symbolic icons or handling high-DPI displays.
Syntax extras like color transformation functions (though some are deprecated in favor of standard CSS).
Media queries (since GTK 4.20) for themes like dark mode (prefers-color-scheme: dark).

Properties can be defined in theme files, inline styles, or via APIs in languages like Python (using GI). For example, in Python:
Pythonimport gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

css = """
button {
background-color: blue;
color: white;
-gtk-icon-palette: success green;
}
"""
provider = Gtk.CssProvider()
provider.load_from_data(css.encode())
Gtk.StyleContext.add_provider_for_display(
Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
All properties support cascade keywords: inherit, initial, unset. Units include px, pt, em, rem (root-based), and physical (in, cm) scaled by -gtk-dpi.
Standard CSS Properties Supported in GTK
GTK supports a wide range of standard CSS properties, primarily from CSS Color, Fonts, Backgrounds, Borders, and Transitions modules. Below is a complete table of these properties, including types/values, animatability (for transitions), inheritance (from parent widgets), and GTK-specific notes.

PropertyType / ValuesAnimatable?Inherited?NotescolorCSS color (rgb, rgba, hsl, hsla, named, etc.)YesYesSets foreground color; supports currentColor, transparent.opacityNumber (0-1 or 0-100%)YesNoWidget transparency.filterCSS filter functions (blur, brightness, etc.)YesNoApplies graphical effects.font-familyComma-separated font namesNoYesDefaults to system font from gtk-font-name setting.font-sizeLength (px, pt, em, rem, etc.)NoYesDefaults to system font size; rem uses initial size.font-stylenormal | italic | obliqueNoYesfont-variantnormal | small-caps (CSS2 values only)NoYesLimited to CSS2; no CSS3 full support.font-weight100-900, normal, bold, etc.NoYesfont-stretchultra-condensed to ultra-expandedNoYesfont-kerningauto | normal | noneNoYesfont-variant-ligaturesnormal | none | common-ligatures, etc.NoYesfont-variant-positionnormal | sub | superNoYesfont-variant-capsnormal | small-caps | all-small-caps, etc.NoYesfont-variant-numericnormal | ordinal | lining-nums, etc.NoYesfont-variant-alternatesnormal | stylistic | historical-forms, etc.NoYesfont-variant-east-asiannormal | jis78 | ruby, etc.NoYesfont-feature-settingsComma-separated feature tagsNoYesOpenType features.font-variation-settingsAxis-value pairsNoYesVariable fonts.caret-colorColorYesYesText insertion point; no 'auto'.letter-spacingLength | normalYesYestext-transformnone | capitalize | uppercase | lowercase (limited)NoYesNo full-width or full-size-kana.line-heightLength | number | normalYesYestext-decoration-linenone | underline | overline | line-throughYesYestext-decoration-colorColorYesYestext-decoration-stylesolid | double | dotted | dashed | wavyYesYestext-shadowShadow list (offset, blur, color)YesYestext-decorationShorthand for line, color, styleYesYestransformTransform functions (translate, scale, rotate, etc.)YesNo2D only; no 3D.transform-originLength/percentage/keywords (top, left, etc.); no z-axisYesNomin-widthLength | percentageYesNoMinimum widget size.min-heightLength | percentageYesNoMinimum widget size.margin-top/right/bottom/leftLength | percentage | autoNoNoExternal spacing.marginShorthand (1-4 values)NoNopadding-top/right/bottom/leftLength | percentageNoNoInternal spacing.paddingShorthand (1-4 values)NoNoborder-top/right/bottom/left-widthLength | thin | medium | thickNoNoborder-top/right/bottom/left-stylenone | solid | dotted | dashed | double | hiddenNoNoNo groove/ridge/inset/outset.border-top/right/bottom/left-colorColorNoNoborder-top/right/bottom/left-radiusLength | percentageNoNoCorner rounding.border-image-sourceurl("image.png") | gradient | noneNoNoSliced border images.border-image-repeatstretch | repeat | round | spaceNoNoborder-image-sliceNumbers/percentage (1-4); fill optionalNoNoborder-image-widthLength/percentage/auto (1-4)NoNoborder-width/style/color/top/right/bottom/leftShorthandsNoNoborder-radiusShorthand (1-4 values)NoNoborder-imageFull shorthandNoNooutline-stylenone | solid | dotted | dashed | double | hiddenNoNoNo auto.outline-widthLength | thin | medium | thickNoNooutline-colorColorNoNoNo invert.outline-offsetLengthNoNooutlineShorthandNoNobackground-colorColorYesNobackground-clipborder-box | padding-box | content-box | textNoNobackground-originpadding-box | border-box | content-boxNoNobackground-sizeLength/percentage/auto/cover/contain (pairs)NoNobackground-positionLength/percentage/keywords (pairs)NoNobackground-repeatrepeat | no-repeat | space | round (pairs)NoNobackground-imageurl("image.jpg") | gradient | none (URLs quoted)NoNoMultiple backgrounds supported.box-shadowShadow list (inset optional)YesNobackground-blend-modenormal | multiply | screen, etc. (per layer)NoNoFor multiple backgrounds.backgroundFull shorthandNoNotransition-property/duration/timing-function/delayAll/standard valuesNoNotransitionShorthandNoNoanimation-name/duration/timing-function/iteration-count/direction/play-state/delay/fill-modeStandard valuesNoNoanimationShorthandNoNoborder-spacingLength (horizontal/vertical)NoNoFor layouts like GtkGridLayout.
GTK-Specific Properties
These are unique to GTK and prefixed with -gtk-. They address GUI-specific needs like icon theming.

PropertyType / ValuesAnimatable?Inherited?Notes-gtk-dpiNumber (pixels per inch)NoNoDefaults to screen DPI; affects physical units like pt/cm.-gtk-icon-source-gtk-icontheme("name") | builtin("name") | noneNoNoSources icons for widgets like buttons.-gtk-icon-sizeLengthNoNoScales builtin icons.-gtk-icon-stylerequested | regular | symbolicNoNoPrefers symbolic for high-contrast themes.-gtk-icon-transformTransform list | noneYesNoRotates/scales icons.-gtk-icon-paletteComma-separated: name color (e.g., error red)NoNoRecolors symbolic icons; defaults map error/warning/success.-gtk-icon-shadowShadow list | noneYesNoAdds shadows to icons.-gtk-icon-filterFilter list | noneYesNoApplies effects to icons.-gtk-icon-weight100-900 | normal | boldYesNoFor stroked symbolic icons.-gtk-secondary-caret-colorColorYesYesFor bidirectional text carets.
Custom Properties and Syntax Extensions
GTK fully supports CSS variables (custom properties) like --my-color: red; color: var(--my-color, blue);. Deprecated legacy syntax includes @define-color for named colors and functions like mix(color1, color2, 0.5) – migrate to standard CSS color-mix().
GTK extensions:

-gtk-icontheme(name): Loads themed icons.
-gtk-recolor(url, palette): Recolors images using -gtk-icon-palette.
-gtk-scaled(image1, image2): Provides resolution variants (e.g., for 2x DPI).

Units, Functions, and Media Queries

Units: Pixel-based (px), font-relative (em, ex, rem), absolute (pt, pc, in, cm, mm scaled by DPI).
Functions: calc() for computations; var() for variables.
Media Queries: @media (prefers-color-scheme: dark) { ... }, (prefers-contrast: high), (prefers-reduced-motion: reduce) (GTK 4.20+).

Best Practices and Considerations

Widget-Specific Nodes: Check docs for each widget (e.g., GtkButton has .text-button class if content is text). Add custom classes via gtk_widget_add_css_class().
Deprecations: Avoid legacy color functions; use CSS4+ equivalents.
Performance: Animations are hardware-accelerated where possible, but complex filters may impact speed.
Testing: Use GTK Inspector (Ctrl+Shift+I in apps) to debug CSS.
Compatibility: GTK3 had similar properties but fewer features; upgrade to GTK4 for modern apps like those using libadwaita.
Resources: For examples, see GNOME themes or apps like GNOME Text Editor.

This reference ensures complete coverage of valid styles, enabling precise widget customization.
