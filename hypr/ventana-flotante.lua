-- hermes-learn: ventana flotante para las explicaciones (Hyprland con config en Lua).
-- Pégalo en ~/.config/hypr/hyprland.lua.
-- Chromium --app recibe su clase real después de mapear la ventana, así que se
-- ajusta por evento en vez de con una regla estática.
local function float_explicacion(w)
  if w == nil or w.class == nil then return end
  if w.class:match("Explicaciones_%d%d%d%d%-%d%d%-%d%d_%d+%.html") then
    hl.dispatch(hl.dsp.window.float({ window = w, action = "enable" }))
    hl.dispatch(hl.dsp.window.resize({ window = w, x = 900, y = 760 }))
    hl.dispatch(hl.dsp.window.center({ window = w }))
  end
end
hl.on("window.class", float_explicacion)
hl.on("window.open", float_explicacion)

-- Atajo (en bindings.lua). En Omarchy, SUPER+SHIFT+E abre HEY: quítalo antes.
-- hl.unbind("SUPER + SHIFT + E")
-- o.bind("SUPER + SHIFT + E", "Explicar portapapeles", "explicar")

-- Hyprland clásico (hyprland.conf), equivalente aproximado:
--   bind = SUPER SHIFT, E, exec, explicar
--   windowrule = float, size 900 760, center, class:^(chrome-.*Explicaciones_.*)$
