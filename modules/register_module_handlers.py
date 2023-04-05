from .start_bot import register_start_handlers
from .keyboards_button import register_button_handlers
from .mines import register_mine_handler
from .admins import register_admin_handlers
from .hotline import register_hotline_handlers
from .bonus import register_bonus_handler
from .echonomy import register_give_value_handlers, register_main_commands_handlers
from .rp import register_rp_commands_handler
from .games import register_rullete_handlers, register_dice_handlers
from .send_ad import register_ad_handlers

def register_module_handler(dp):
    register_ad_handlers(dp)
    register_dice_handlers(dp)
    register_rullete_handlers(dp)
    register_rp_commands_handler(dp)
    register_main_commands_handlers(dp)
    register_give_value_handlers(dp)
    register_bonus_handler(dp)
    register_admin_handlers(dp)
    register_hotline_handlers(dp)
    register_mine_handler(dp)
    register_button_handlers(dp)
    register_start_handlers(dp)
