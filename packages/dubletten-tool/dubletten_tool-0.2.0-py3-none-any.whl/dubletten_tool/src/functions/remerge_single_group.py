from dubletten_tool.src.classes import MergeGroup, function_timer, TempRel, ErrorLoggerMixin, PersonHelper, PPHelper, logger, rt_vorfin, time, ProcessingTracker, RelationWriter


def remerge_single_group(group, vorfins=None):
    """
    Todo: wrap in error handling that resets all classes accordingly (would be a use-case for a context-manager)
    Todo: fetch the re-created and or changed rel data-frames and display them in browser after remerge.
    """

    # setup classes
    TempRel.setup()
    RelationWriter.setup()
    PersonHelper.update_collections()

    if not vorfins:
        old_vorfin = group.vorfin

        # fetch and store all relations from old vorfin
        if old_vorfin:
            all_rels = old_vorfin.get_related_relation_instances()
            for rel in all_rels:
                if rel.relation_type != rt_vorfin:
                    TempRel(rel)

    else: 
        all_rels = []
        for vorfin in vorfins:
            v_rels = vorfin.get_related_relation_instances()
            all_rels += [rel for rel in v_rels if rel.relation_type != rt_vorfin]

        [TempRel(rel) for rel in all_rels]


    # create new vorfin
    
    mg = MergeGroup(group)
    mg.run_process()


    # Update the PersonHelper collections to include new vorfin
    # TODO: old vorfin or vorfins must be deleted, before updating collections
    PersonHelper.update_collections()


    # create perper relations
    try:
        RelationWriter.write_person_person_rels(group)
    except Exception as e:
        logger.exception(e)

    ProcessingTracker.log()

    if not vorfins and old_vorfin:
        # TODO: I think this is in the wrong place. The old vorfins must be deleted before the collections are updated.
    # delete old vorfin
        old_vorfin.delete()
    elif not vorfins and not old_vorfin: 
        print("vorfins was false and no old_vorfin")
    else: 
        print("vorfins true, old vorfin false")
        [v.delete() for v in vorfins]


    # re-write old relations
    # TODO: test what happens on merg of new group, that has no vorfin and no vorfins. IF this can even happen.
    TempRel.re_create_rels()
    TempRel.log_stats_report()
    RelationWriter.log_report()
    RelationWriter.log_details()

    # show which relations where re-added
    # TODO: export logs and xlsx files and offer them to download or display as html table in frontend
    # - use pandas to_html method ---

    changed_vorfins = TempRel.get_changed_edited_vorfins_dataframe()
    created_rels = TempRel.get_created_rels_dataframe()

    # reset all used classes and free the memory
    TempRel.reset()
    RelationWriter.reset()
    # ErrorLoggerMixin needs special treatment here

    # return vorfin
    new_vorfin = mg.person

    print("new_vorfin id ", new_vorfin.id)
    return {"new_vorfin": new_vorfin, "new_vorfin_id": str(new_vorfin.id), "changed_vorfins": changed_vorfins, "created_rels": created_rels}
