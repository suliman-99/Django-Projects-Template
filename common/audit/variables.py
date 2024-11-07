

audit_fields = (
    'created_at',
    'created_by',
    'updated_at',
    'updated_by',
    'deleted',
    'deleted_by_cascade',
)


audit_read_only_kwargs = {
    'created_at': { 'read_only': True },
    'created_by': { 'read_only': True },
    'updated_at': { 'read_only': True },
    'updated_by': { 'read_only': True },
    'deleted': { 'read_only': True },
    'deleted_by_cascade': { 'read_only': True },
}
