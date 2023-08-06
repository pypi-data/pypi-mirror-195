from .constants import DIRECTIVES
from checker.checker.src import doc_as_code

def check_traceability_links(needs, need, needs_flow_link_types, log):
    if not needs:
        return False
    allowed_links = DIRECTIVES.get(need['type'])
    if allowed_links is None or not allowed_links:
        return False
    for link_type in needs_flow_link_types:
        if need[link_type]:
            links = need[link_type]
            for link in links:
                target_need = needs[link]
                target_need_type = target_need['type']
                if target_need_type not in allowed_links:
                    log.warn(f"Directive {need['type']} cannot be associated "
                             f"with directive {target_need_type}. the allowed directive(s) of {need['type']} is/are "
                             f"{allowed_links}")
                    return True
    return False

##
#
# @rst
# :need: REQ_1

# .. req:: My #11 requirement
#     :id: REQ_11
#     :status: draft
#     :tags: example
#
#     This need is a requirement, and it includes a title, an ID, a Tag and this test as a description.
#
#     We didn't set the **ID** option here, so **Sphinx-Needs** will generate one for us.
#     But we have set a **link** to our previous requirement and have set the **status** option.
#     Also, we have enabled **collapse** to false to show all meta-data directly under the title.
# @endrst

class Helper:

    def __init__(self):
        print("hallo")

    ##
    #
    # @rst
    # .. req:: A more complex and highlighted requirement
    #   :id: REQ_3
    #   :status: open
    #   :tags: awesome, nice, great
    #   :links: REQ_1
    #   :layout: complete
    #   :style: red_border

    #   More columns for better data structure and a red border.
    # @endrst
    def fun_helper():
        return 0