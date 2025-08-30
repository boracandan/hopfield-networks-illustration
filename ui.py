import pygame_gui as pg
import pygame
from math import ceil

class UIButton(pg.elements.UIButton):
    def __init__(self, relative_rect, text, manager = None, container = None, tool_tip_text = None, starting_height = 1, parent_element = None, object_id = None, anchors = None, allow_double_clicks = False, generate_click_events_from = (1,), visible = 1, *, command = None, tool_tip_object_id = None, text_kwargs = None, tool_tip_text_kwargs = None, max_dynamic_width = None, toggle_button = False, brighten_amount=40) -> None:
        super().__init__(relative_rect, text, manager, container, tool_tip_text, starting_height, parent_element, object_id, anchors, allow_double_clicks, generate_click_events_from, visible, command=command, tool_tip_object_id=tool_tip_object_id, text_kwargs=text_kwargs, tool_tip_text_kwargs=tool_tip_text_kwargs, max_dynamic_width=max_dynamic_width)
        self._toggleButton = toggle_button
        self._toggled = False
        self._tint_off = self.colours['normal_bg']

        # Brighten directly in __init__
        c = self._tint_off
        r = min(c.r + brighten_amount, 255)
        g = min(c.g + brighten_amount, 255)
        b = min(c.b + brighten_amount, 255)
        self._tint_on = pygame.Color(r, g, b)

    @property
    def toggled(self) -> bool:
        return self._toggled
    
    def toggle(self) -> None:
        if not self._toggleButton:
            return
        self._toggled = not self.toggled
        self.colours['normal_bg'] = self._tint_on if self._toggled else self._tint_off
        self.rebuild()

   
class ToggleButtonGroup:
    def __init__(self, buttons: list[UIButton]) -> None:
        self.buttons = buttons

    def process_event(self, event: pygame.Event) -> None:
        if (
            event.type == pygame.USEREVENT and
            event.user_type == pg.UI_BUTTON_PRESSED and
            event.ui_element in self.buttons
        ):
            pressed_button = event.ui_element
            # Toggle pressed button ON
            pressed_button.toggle()
            # Toggle others OFF
            for btn in self.buttons:
                if btn != pressed_button and btn.toggled:
                    btn.toggle()

class UI:
    def __init__(self, rect: pygame.FRect, manager: pg.UIManager, memory_num: int) -> None:
        self.width, self.height = rect.size
        
        panel_rect = rect.copy()
        panel_rect.height -= int(self.height * 0.075)
        self.ui_panel = pg.elements.UIPanel(
            relative_rect=panel_rect,
            manager=manager
        )

        # Mode Select Buttons
        self.pert_mode_button = UIButton(
            relative_rect=pygame.FRect(panel_rect.bottomleft - pygame.Vector2(0, 4), (self.width * .5, self.height * .08)),
            text="Perturb Mode",
            manager=manager
        )

        self.recog_mode_button = UIButton(
            relative_rect=pygame.FRect(self.pert_mode_button.rect.topright - pygame.Vector2(4, 0), (self.width * .52, self.height * .08)),
            text="Recog Mode",
            manager=manager
        )

        #-----Perturbing Mode UI------#
        
        self.pert_mode_panel = pg.elements.UIPanel(
            relative_rect=pygame.FRect((-2, -2), (self.width, self.height)),
            manager=manager,
            container=self.ui_panel,
        )
                
        self.modern_button = UIButton(
            relative_rect=pygame.FRect((self.width * .15, self.height * 0.0075), (self.width  * .7, self.height * .05)),
            text="Modern Hopfield",
            manager=manager,
            container=self.pert_mode_panel,
            toggle_button=True,
        )
        
        self.classical_button = UIButton(
            relative_rect=pygame.FRect((self.width * .15, self.height * 0.06), (self.width  * .7, self.height * .05)),
            text="Classical Hopfield",
            manager=manager,
            container=self.pert_mode_panel,
            toggle_button=True
        )

        self.pert_button_group = ToggleButtonGroup([self.modern_button, self.classical_button])

        self.memory_label = pg.elements.UILabel(
            relative_rect=pygame.FRect((self.width * .08, self.height * 0.12), (self.width * .55, self.height * .05)),
            manager=manager,
            container=self.pert_mode_panel,
            text="Memory Images:"
        )
        
        self.memory_buttons = []
        memory_rect = pygame.FRect((self.width * .05, self.height * 0.16), (self.width * .92, self.height * .2))
        num_cols = 5
        num_rows = ceil(memory_num / num_cols)
        padding = 0.03  # 3% padding inside memory_rect

        for i in range(memory_num):
            row = i // num_cols
            col = i % num_cols
            btn_width = (memory_rect.width * (1 - padding * 2)) / num_cols
            btn_height = (memory_rect.height * (1 - padding * 2)) / num_rows
            btn_x = memory_rect.x + padding * memory_rect.width + col * btn_width
            btn_y = memory_rect.y + padding * memory_rect.height + row * btn_height

            btn = pg.elements.UIButton(
                relative_rect=pygame.FRect((btn_x, btn_y), (btn_width, btn_height)),
                manager=manager,
                container=self.pert_mode_panel,
                text=str(i + 1)
            )
            self.memory_buttons.append(btn)

        self.recall_button = UIButton(
            relative_rect=pygame.FRect((self.width * .15, self.height * 0.4), (self.width  * .7, self.height * .05)),
            text="Recall",
            manager=manager,
            container=self.pert_mode_panel,
        )



        #-----Recognizing Mode UI------#

        # self.recog_mode_panel = pg.elements.UIPanel(
        #     relative_rect=pygame.Rect(left_top=(0, 0), width_height=rect.size),
        #     manager=manager,
        #     container=self.ui_panel,
        #     visible=False
        # )

    def process_event(self, event: pygame.Event) -> None:
        self.pert_button_group.process_event(event)



