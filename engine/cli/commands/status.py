"""
Status command - Display progress status.
"""

from ..loaders import scan_modules, scan_campaigns, load_ledger
from ..core import compute_progress, format_progress


def cmd_status(args):
    """Display progress status based on scope."""
    print("\n=== Scholar Status ===\n")
    
    # Load all data
    modules = scan_modules()
    campaigns = scan_campaigns()
    completed = load_ledger()
    
    print("\n--- Progress Report ---\n")
    
    # Compute based on scope
    if args.scope == "total":
        _show_total_progress(modules, completed)
    elif args.scope == "module":
        _show_module_progress(args.id, modules, completed)
    elif args.scope == "campaign":
        _show_campaign_progress(args.id, campaigns, completed)
    
    print()


def _show_total_progress(modules, completed):
    """Show total progress across all modules."""
    all_assignments = set()
    for assignments in modules.values():
        all_assignments.update(assignments)
    
    progress = compute_progress(all_assignments, completed)
    print(f"Total Progress: {format_progress(progress)}")
    print(f"  Completed: {len(all_assignments & completed)} / {len(all_assignments)}")


def _show_module_progress(module_id, modules, completed):
    """Show progress for a specific module or all modules."""
    if module_id and module_id in modules:
        relevant = set(modules[module_id])
        progress = compute_progress(relevant, completed)
        print(f"Module [{module_id}]: {format_progress(progress)}")
        print(f"  Completed: {len(relevant & completed)} / {len(relevant)}")
    else:
        # Show all modules
        for mid, assignments in modules.items():
            relevant = set(assignments)
            progress = compute_progress(relevant, completed)
            done = len(relevant & completed)
            print(f"  {mid}: {format_progress(progress)} ({done}/{len(relevant)})")


def _show_campaign_progress(campaign_id, campaigns, completed):
    """Show progress for a specific campaign or all campaigns."""
    if campaign_id and campaign_id in campaigns:
        relevant = set(campaigns[campaign_id])
        progress = compute_progress(relevant, completed)
        print(f"Campaign [{campaign_id}]: {format_progress(progress)}")
        print(f"  Completed: {len(relevant & completed)} / {len(relevant)}")
    else:
        # Show all campaigns
        for cid, assignments in campaigns.items():
            relevant = set(assignments)
            progress = compute_progress(relevant, completed)
            done = len(relevant & completed)
            print(f"  {cid}: {format_progress(progress)} ({done}/{len(relevant)})")
