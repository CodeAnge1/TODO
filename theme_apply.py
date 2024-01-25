import dearpygui.dearpygui as dpg

import theme_config as th


def create_theme_custom_theme():
    with dpg.theme() as theme_id:
        with dpg.theme_component(0):
            dpg.add_theme_color(dpg.mvThemeCol_Text, th.mvthemecol_text)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, th.mvthemecol_textdisabled)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, th.mvthemecol_windowbg)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, th.mvthemecol_childbg)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, th.mvthemecol_popupbg)
            dpg.add_theme_color(dpg.mvThemeCol_Border, th.mvthemecol_border)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, th.mvthemecol_bordershadow)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, th.mvthemecol_framebg)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, th.mvthemecol_framebghovered)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, th.mvthemecol_framebgactive)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, th.mvthemecol_titlebg)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, th.mvthemecol_titlebgactive)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, th.mvthemecol_titlebgcollapsed)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, th.mvthemecol_menubarbg)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, th.mvthemecol_scrollbarbg)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, th.mvthemecol_scrollbargrab)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, th.mvthemecol_scrollbargrabhovered)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, th.mvthemecol_scrollbargrabactive)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, th.mvthemecol_checkmark)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, th.mvthemecol_slidergrab)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, th.mvthemecol_slidergrabactive)
            dpg.add_theme_color(dpg.mvThemeCol_Button, th.mvthemecol_button)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, th.mvthemecol_buttonhovered)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, th.mvthemecol_buttonactive)
            dpg.add_theme_color(dpg.mvThemeCol_Header, th.mvthemecol_header)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, th.mvthemecol_headerhovered)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, th.mvthemecol_headeractive)
            dpg.add_theme_color(dpg.mvThemeCol_Separator, th.mvthemecol_separator)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, th.mvthemecol_separatorhovered)
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, th.mvthemecol_separatoractive)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, th.mvthemecol_resizegrip)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, th.mvthemecol_resizegriphovered)
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, th.mvthemecol_resizegripactive)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, th.mvthemecol_tab)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, th.mvthemecol_tabhovered)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, th.mvthemecol_tabactive)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, th.mvthemecol_tabunfocused)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, th.mvthemecol_tabunfocusedactive)
            dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, th.mvthemecol_dockingpreview)
            dpg.add_theme_color(dpg.mvThemeCol_DockingEmptyBg, th.mvthemecol_dockingemptybg)
            dpg.add_theme_color(dpg.mvThemeCol_PlotLines, th.mvthemecol_plotlines)
            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, th.mvthemecol_plotlineshovered)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, th.mvthemecol_plothistogram)
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, th.mvthemecol_plothistogramhovered)
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, th.mvthemecol_tableheaderbg)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, th.mvthemecol_tableborderstrong)
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, th.mvthemecol_tableborderlight)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, th.mvthemecol_tablerowbg)
            dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, th.mvthemecol_tablerowbgalt)
            dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, th.mvthemecol_textselectedbg)
            dpg.add_theme_color(dpg.mvThemeCol_DragDropTarget, th.mvthemecol_dragdroptarget)
            dpg.add_theme_color(dpg.mvThemeCol_NavHighlight, th.mvthemecol_navhighlight)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingHighlight, th.mvthemecol_navwindowinghighlight)
            dpg.add_theme_color(dpg.mvThemeCol_NavWindowingDimBg, th.mvthemecol_navwindowingdimbg)
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, th.mvthemecol_modalwindowdimbg)
            dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.07 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.50 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_PlotBorder, (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBg, (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendBorder, (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_LegendText, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_TitleText, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_InlayText, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_XAxis, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_XAxisGrid, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.25 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.25 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis2, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid2, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.25 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxis3, (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid3, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.25 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Selection, (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Query, (0.00 * 255, 1.00 * 255, 0.44 * 255, 1.00 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs, (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.50 * 255),
                                category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackground, (50, 50, 50, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundHovered, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeBackgroundSelected, (75, 75, 75, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_NodeOutline, (100, 100, 100, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBar, (41, 74, 122, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Link, (61, 133, 224, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkHovered, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_LinkSelected, (66, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_Pin, (53, 150, 250, 180), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_PinHovered, (53, 150, 250, 255), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelector, (61, 133, 224, 30), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_BoxSelectorOutline, (61, 133, 224, 150), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridBackground, (40, 40, 50, 200), category=dpg.mvThemeCat_Nodes)
            dpg.add_theme_color(dpg.mvNodeCol_GridLine, (200, 200, 200, 40), category=dpg.mvThemeCat_Nodes)

    return theme_id
