import click

from patch.auth.auth_forms import AuthForm
from patch.cli.phone_number_param_type import PhoneNumberParamType
from patch.cli.styled import StyledCommand
from patch.cli.commands import pass_obj
from patch.cli import PatchClickContext


@click.command(cls=StyledCommand, help='Login to Patch using your mobile phone or email')
@click.argument('depreciated_phone', required=False, type=PhoneNumberParamType())
@click.option('--email', help='Login to Patch using your email', type=click.STRING)
@click.option('--phone', help='Login to Patch using your mobile phone', type=PhoneNumberParamType())

@pass_obj()
def login(patch_ctx: PatchClickContext, email, phone, depreciated_phone):
    console = patch_ctx.console
    if email:
        auth = AuthForm(email, "email")
        auth.request_validation()
    elif phone:
        auth = AuthForm(phone, "sms")
        auth.request_validation()
    elif depreciated_phone:
        auth = AuthForm(depreciated_phone, "sms")
        auth.request_validation()
        console.print("[yellow]Warning: This method of login is depreciated. Please use --phone to login with a phone number or --email to login with email[/yellow]")
    else:
        console.print("[red]Error: Please login with phone number (--phone) or email (--email)[/red]")
