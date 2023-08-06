'''assemble application'''
# import EPAM_Flask.micropeutist_app.views.web_view # pylint: disable=unused-import
# import EPAM_Flask.micropeutist_app.rest.api_view # pylint: disable=unused-import

import micropeutist_app.views.web_view
import micropeutist_app.rest.api_view
from .config import app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
