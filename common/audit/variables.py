

audit_fields = (
    'deleted',

    'created_at',
    'updated_at',

    'created_by',
    'updated_by',
)


audit_read_only_kwargs = {
    'deleted': { 'read_only': True },

    'created_at': { 'read_only': True },
    'updated_at': { 'read_only': True },

    'created_by': { 'read_only': True },
    'updated_by': { 'read_only': True },
}
