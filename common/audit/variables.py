

audit_fields = (
    'created_at',
    'created_by',

    'updated_at',
    'updated_by',

    'deleted_at',
    'deleted_by',

    'is_deleted',
)


audit_read_only_kwargs = {
    'created_at': { 'read_only': True },
    'created_by': { 'read_only': True },

    'updated_at': { 'read_only': True },
    'updated_by': { 'read_only': True },

    'deleted_at': { 'read_only': True },
    'deleted_by': { 'read_only': True },
}
