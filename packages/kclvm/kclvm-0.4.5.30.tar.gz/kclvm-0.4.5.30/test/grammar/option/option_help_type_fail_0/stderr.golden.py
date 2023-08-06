
import sys
import kclvm.kcl.error as kcl_error
import os

cwd = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(cwd, 'main.k')

kcl_error.print_kcl_error_message(
    kcl_error.get_exception(err_type=kcl_error.ErrType.EvaluationError_TYPE,
                            file_msgs=[
                                kcl_error.ErrFileMsg(
                                    filename=file,
                                    line_no=1,
                                ),
                            ],
                            arg_msg=f"option('name') must be initialized, try '-D name=?' argument")
    , file=sys.stdout
)

