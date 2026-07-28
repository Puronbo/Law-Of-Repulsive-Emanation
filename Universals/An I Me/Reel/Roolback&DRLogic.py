class RollbackCoordinator:
    def authorize_rollback(self, epoch, n_nodes, current_votes):
        if len(current_votes) > (n_nodes / 2):
            return True
        return False

class BootstrapHandler:
    async def process_bootstrap(self, snapshot_id, new_epoch, store):
        store.clear_uncommitted()
        store.load_snapshot(snapshot_id)
        return new_epoch