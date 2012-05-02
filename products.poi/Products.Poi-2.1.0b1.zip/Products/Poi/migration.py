import logging
import sets

from ZODB.POSException import ConflictError
from Products.CMFCore.utils import getToolByName
from Products.CMFFormController.FormAction import FormActionKey
from zope.publisher.browser import TestRequest
import transaction

from Products.Poi.interfaces import IIssue
from Products.Poi.adapters import Response
from Products.Poi.adapters import IResponseContainer
from Products.Poi.browser.response import Create


logger = logging.getLogger("Poi")
PROFILE_ID = 'profile-Products.Poi:default'


def migrate_workflow_changes(context):
    """Migrate workflow changes from ids to titles.

    When a response changes the workflow state of an issue, this
    change is recorded in that response.  This used to be done by
    storing review state ids.  Currently this is done by storing
    review state titles.  Friendlier for the end user and translatable
    to boot.  This migration finds responses with review state ids in
    them and turns them into titles.
    """
    logger.info("Starting migration of workflow changes.")
    catalog = getToolByName(context, 'portal_catalog')
    wftool = getToolByName(context, 'portal_workflow')

    def get_state_title(state_id):
        # This neatly returns the input when there is no such review
        # state id, which happens when the 'state_id' is already a
        # title.
        return wftool.getTitleForStateOnType(state_id, 'PoiIssue')

    issue_brains = catalog.searchResults(portal_type='PoiIssue')
    logger.info("Found %s PoiIssues.", len(issue_brains))
    fixed = 0
    for brain in issue_brains:
        try:
            issue = brain.getObject()
        except (AttributeError, KeyError):
            logger.warn("AttributeError or KeyError getting tracker object at "
                        "%s", brain.getURL())
            continue
        folder = IResponseContainer(issue)
        made_changes = False
        for response in folder:
            for change in response.changes:
                #def add_change(self, id, name, before, after):
                if change['id'] != 'review_state':
                    continue
                before = get_state_title(change['before'])
                if change['before'] != before:
                    made_changes = True
                    change['before'] = before
                change['after'] = get_state_title(change['after'])
        if made_changes:
            fixed += 1
            if fixed % 100 == 0:
                logger.info("Committing transaction after fixing "
                            "%s PoiIssues; still busy... " % fixed)
                transaction.commit()
    logger.info("Migration completed.  %s PoiIssues needed fixing.", fixed)


def run_workflow_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'workflow')
    # Run the update security on the workflow tool.
    logger.info('Updating security settings.  This may take a while...')
    wf_tool = getToolByName(context, 'portal_workflow')
    wf_tool.updateRoleMappings()
    logger.info('Done updating security settings.')


def update_tracker_managers(context, testing=False):
    """Make sure all managers of a tracker get the TrackerManager role.

    We used to give users in the 'managers' field of a tracker the
    local Manager role.  Now we give them the new TrackerManager role.
    In this upgrade step we remove the local Manager role from all
    users.  Instead we give them the TrackerManager role.  This might
    give a few 'false positives', where a user has been intentionally
    given the local Manager role and will now lose it.  That can't be
    helped and is not expected to be a big problem.

    If testing is True, do not commit; this avoids some problems when
    running the tests.
    """
    logger.info("Starting update of tracker managers.")
    catalog = getToolByName(context, 'portal_catalog')
    tracker_brains = catalog.searchResults(
        portal_type=('PoiTracker', 'PoiPscTracker'))
    logger.info("Found %s PoiTrackers.", len(tracker_brains))
    for brain in tracker_brains:
        try:
            tracker = brain.getObject()
        except (AttributeError, KeyError):
            logger.warn("AttributeError or KeyError getting tracker object at "
                        "%s", brain.getURL())
            continue

        field = tracker.getField('managers')
        managers = field.get(tracker)
        tracker_changed = False
        for user_id in managers:
            user_changed = False
            local_roles = list(tracker.get_local_roles_for_userid(user_id))
            if 'Manager' in local_roles:
                logger.info("Removing local Manager role from user %s.",
                            user_id)
                local_roles.remove('Manager')
                user_changed = True
            if not 'TrackerManager' in local_roles:
                logger.info("Giving user %s TrackerManager role.", user_id)
                local_roles.append('TrackerManager')
                user_changed = True
            if user_changed:
                tracker.manage_setLocalRoles(user_id, local_roles)
                tracker_changed = True
        if tracker_changed and not testing:
            logger.info("Committing after updating roles on tracker %s",
                        tracker.absolute_url())
            transaction.commit()


def remove_form_controller_action(context):
    """Remove our action from the portal_form_controller.

    We used to add the poi_issue_post action (a skin script) to the
    validate_integrity script.  Now we have registered an event
    handler instead so the action is no longer needed.  And we have
    removed the skin script, so we must remove the action as otherwise
    anyone submitting a new issue will get an error.
    """
    controller = getToolByName(context, 'portal_form_controller')
    action_key = FormActionKey('validate_integrity', 'success', 'PoiIssue', '')
    try:
        action = controller.actions.get(action_key)
    except KeyError:
        logger.info("Action for validate_integrity not found; ignoring.")
        return
    if action.getActionArg() != 'string:poi_issue_post':
        logger.info("Expected action argument 'string:poi_issue_post' for "
                    "successfull validate_integrity on PoiIssue; found %r "
                    "instead; ignoring.", action.getActionArg())
        return
    try:
        controller.actions.delete(action_key)
    except (ConflictError, KeyboardInterrupt):
        raise
    except Exception, exc:
        # This way of removing an action is yucky; I wonder how many
        # things can go wrong; let's inform the user.
        url = controller.absolute_url() + '/manage_formActionsForm'
        error = ("Exception while removing action poi_issue_post on "
                 "validate_integrity. Please go to %s and remove it manually. "
                 "Original exception was: %r" % (url, exc))
        raise Exception(error)
    else:
        logger.info("Removed action poi_issue_post from validate_integrity.")


def run_rolemap_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'rolemap')


def run_sharing_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'sharing')


def run_types_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')


def purge_workflow_scripts(context):
    """Remove reference to old workflow scripts.

    We used to have some external methods hooked up to the issue
    workflow, but this is now done with events.  Having the scripts
    mentioned in the ZMI does not seem to cause problems, but it is
    cleaner to remove them, as we do not need them.  Also, a workflow
    export and import would fail.
    """
    wf_tool = getToolByName(context, 'portal_workflow')
    wf_id = 'poi_issue_workflow'
    bad_scripts = ('sendInitialEmail', 'sendResolvedMail')
    wf = wf_tool.getWorkflowById(wf_id)
    for script_name in bad_scripts:
        if script_name in wf.scripts.objectIds():
            wf.scripts._delObject(script_name)
            logger.info('Removed script %s from %s', script_name, wf_id)


def run_javascript_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
