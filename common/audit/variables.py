

audit_fields = (
    'created_at',
    'updated_at',
    'deleted',
)


audit_read_only_kwargs = {
    'created_at': { 'read_only': True },
    'updated_at': { 'read_only': True },
    'deleted': { 'read_only': True },
}
