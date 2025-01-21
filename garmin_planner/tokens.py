# Reserved words
reserved = {
    'cal': 'CALORIES',
    'power': 'POWER',
    'bpm': 'BPM',
    'spm': 'SPM',
    'hr': 'HR',
    'zone': 'ZONE',
    'w': 'WATTS',
    'run': 'RUN',
    'strength': 'STRENGTH',
    'warmup': 'WARMUP',
    'cooldown': 'COOLDOWN',
    'recover': 'RECOVER',
    'rest': 'REST',
    'other': 'OTHER',
    'above': 'ABOVE',
    'below': 'BELOW',
    'intensities': 'INTENSITIES',
    'durations': 'DURATIONS',
    'garmin': 'GARMIN',
    'username': 'USERNAME',
    'password': 'PASSWORD'
}

# Token definitions
tokens = [
    'LBRACKET',
    'RBRACKET',
    'HYPHEN',
    'AT',
    'TIME',
    'INT',
    'INT_REP',
    'FLOAT',
#     'TIMES',
    'ID',
    'STRING'
] + list(reserved.values())