KOBO_MAPPINGS = {
    'fistula_campaign': {
        'model': 'tracker.FistulaCase',
        'fields': {
            'age': 'age',
            'district': 'district',
            'upazila': 'upazila',
            'referral_status': 'referral_status',
            'surgery_outcome': 'surgery_outcome',
            'has_disability': 'has_disability',
            'is_ethnic_minority': 'is_ethnic_minority',
            'is_displaced': 'is_displaced',
        }
    },
    'mpdsr_report': {
        'model': 'mpdsr.MPDSREvent',
        'fields': {
            'death_type': 'death_type',
            'age_of_deceased': 'age_of_deceased',
            'district': 'district',
            'facility_name': 'facility_name',
            'cause_of_death': 'cause_of_death',
            'social_autopsy_findings': 'social_autopsy_findings',
            'recommended_action': 'recommended_action',
            'action_status': 'action_status',
        }
    }
}
