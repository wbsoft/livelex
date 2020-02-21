# -*- coding: utf-8 -*-
#
# This file is part of the parce Python package.
#
# Copyright © 2019-2020 by Wilbert Berendsen <info@wilbertberendsen.nl>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
LilyPond words. To be generated somehow.

For now, markup commands.

"""

keywords = (
    'accepts',
    'alias',
    'consists',
    'defaultchild',
    'denies',
    #'description',
    #'grobdescriptions',
    'hide', # since 2.18
    'include',
    #'invalid',
    'language',
    'name',
    #'objectid',
    'omit', # since 2.18
    'once',
    'set',
    'unset',
    'override',
    'revert',
    'remove',
    'temporary', # since 2.18
    'sequential',
    'simultaneous',
    #'type',
    'undo', # since 2.18 (not mentioned in the command index)
    'version',
    'score',
    'book',
    'bookpart',
    'header',
    'paper',
    'midi',
    'layout',
    'with',
    'context',
)


markupcommands_nargs = (
# no arguments
(
    'doubleflat',
    'doublesharp',
    'eyeglasses',
    'flat',
    'natural',
    'null',
    'semiflat',
    'semisharp',
    'sesquiflat',
    'sesquisharp',
    'sharp',
    'strut',
    'table-of-contents'
),
# one argument
(
    'backslashed-digit',
    'bold',
    'box',
    'bracket',
    'caps',
    'center-align',
    'center-column',
    'char',
    'circle',
    'column',
    'concat',
    'dir-column',
    'draw-dashed-line', # since 2.18
    'draw-dotted-line', # since 2.18
    'draw-line',
    'dynamic',
    'fill-line',
    'finger',
    'fontCaps',
    'fret-diagram',
    'fret-diagram-terse',
    'fret-diagram-verbose',
    'fromproperty',
    'harp-pedal',
    'hbracket',
    'hspace',
    'huge',
    'italic',
    'justify',
    'justify-field',
    'justify-string',
    'large',
    'larger',
    'left-align',
    'left-brace',
    'left-column',
    'line',
    'lookup',
    'markalphabet',
    'markletter',
    'medium',
    'musicglyph',
    'normalsize',
    'normal-size-sub',
    'normal-size-super',
    'normal-text',
    'number',
    'oval', # since 2.18
    'postscript',
    'right-align',
    'right-brace',
    'right-column',
    'roman',
    'rounded-box',
    'sans',
    'score',
    'simple',
    'slashed-digit',
    'small',
    'smallCaps',
    'smaller',
    'stencil',
    'sub',
    'super',
    'teeny',
    'text',
    'tied-lyric',
    'tiny',
    'transparent',
    'triangle',
    'typewriter',
    'underline',
    'upright',
    'vcenter',
    'vspace',
    'verbatim-file',
    'whiteout',
    'wordwrap',
    'wordwrap-field',
    'wordwrap-string',
),
# two arguments
(
    'abs-fontsize',
    'auto-footnote', # since 2.16
    'combine',
    'customTabClef',
    'fontsize',
    'footnote',
    'fraction',
    'halign',
    'hcenter-in',
    'lower',
    'magnify',
    'note',
    'on-the-fly',
    'override',
    'pad-around',
    'pad-markup',
    'pad-x',
    'page-link',
    'path',     # added in LP 2.13.31
    'raise',
    'rotate',
    'scale',
    'translate',
    'translate-scaled',
    'with-color',
    'with-link',
    'with-url',
    'woodwind-diagram',
),
# three arguments
(
    'arrow-head',
    'beam',
    'draw-circle',
    'epsfile',
    'filled-box',
    'general-align',
    'note-by-number',
    'pad-to-box',
    'page-ref',
    'with-dimensions',
),
# four arguments
(
    'pattern',
    'put-adjacent',
),
# five arguments,
(
    'fill-with-pattern',
),
)

markupcommands = sum(markupcommands_nargs, ())

contexts = (
    'ChoirStaff',
    'ChordNames',
    'CueVoice',
    'Devnull',
    'DrumStaff',
    'DrumVoice',
    'Dynamics',
    'FiguredBass',
    'FretBoards',
    'Global',
    'GrandStaff',
    'GregorianTranscriptionStaff',
    'GregorianTranscriptionVoice',
    'KievanStaff', # since 2.16
    'KievanVoice', # since 2.16
    'Lyrics',
    'MensuralStaff',
    'MensuralVoice',
    'NoteNames',
    'NullVoice',     # since 2.18
    'PetrucciStaff', # since 2.16
    'PetrucciVoice', # since 2.16
    'PianoStaff',
    'RhythmicStaff',
    'Score',
    'Staff',
    'StaffGroup',
    'TabStaff',
    'TabVoice',
    'Timing',
    'VaticanaStaff',
    'VaticanaVoice',
    'Voice',
)

grobs = (
    'Accidental',
    'AccidentalCautionary',
    'AccidentalPlacement',
    'AccidentalSuggestion',
    'Ambitus',
    'AmbitusAccidental',
    'AmbitusLine',
    'AmbitusNoteHead',
    'Arpeggio',
    'BalloonTextItem',
    'BarLine',
    'BarNumber',
    'BassFigure',
    'BassFigureAlignment',
    'BassFigureAlignmentPositioning',
    'BassFigureBracket',
    'BassFigureContinuation',
    'BassFigureLine',
    'Beam',
    'BendAfter',
    'BreakAlignGroup',
    'BreakAlignment',
    'BreathingSign',
    'ChordName',
    'Clef',
    'ClefModifier',
    'ClusterSpanner',
    'ClusterSpannerBeacon',
    'CombineTextScript',
    'CueClef',
    'CueEndClef',
    'Custos',
    'DotColumn',
    'Dots',
    'DoublePercentRepeat',
    'DoublePercentRepeatCounter',
    'DoubleRepeatSlash',
    'DynamicLineSpanner',
    'DynamicText',
    'DynamicTextSpanner',
    'Episema',
    'Fingering',
    'FingeringColumn',
    'Flag',
    'FootnoteItem',
    'FootnoteSpanner',
    'FretBoard',
    'Glissando',
    'GraceSpacing',
    'GridLine',
    'GridPoint',
    'Hairpin',
    'HorizontalBracket',
    'InstrumentName',
    'InstrumentSwitch',
    'KeyCancellation',
    'KeySignature',
    'KievanLigature',
    'LaissezVibrerTie',
    'LaissezVibrerTieColumn',
    'LedgerLineSpanner',
    'LeftEdge',
    'LigatureBracket',
    'LyricExtender',
    'LyricHyphen',
    'LyricSpace',
    'LyricText',
    'MeasureCounter',
    'MeasureGrouping',
    'MelodyItem',
    'MensuralLigature',
    'MetronomeMark',
    'MultiMeasureRest',
    'MultiMeasureRestNumber',
    'MultiMeasureRestText',
    'NonMusicalPaperColumn',
    'NoteCollision',
    'NoteColumn',
    'NoteHead',
    'NoteName',
    'NoteSpacing',
    'OttavaBracket',
    'PaperColumn',
    'ParenthesesItem',
    'PercentRepeat',
    'PercentRepeatCounter',
    'PhrasingSlur',
    'PianoPedalBracket',
    'RehearsalMark',
    'RepeatSlash',
    'RepeatTie',
    'RepeatTieColumn',
    'Rest',
    'RestCollision',
    'Script',
    'ScriptColumn',
    'ScriptRow',
    'Slur',
    'SostenutoPedal',
    'SostenutoPedalLineSpanner',
    'SpacingSpanner',
    'SpanBar',
    'SpanBarStub',
    'StaffGrouper',
    'StaffSpacing',
    'StaffSymbol',
    'StanzaNumber',
    'Stem',
    'StemStub',
    'StemTremolo',
    'StringNumber',
    'StrokeFinger',
    'SustainPedal',
    'SustainPedalLineSpanner',
    'System',
    'SystemStartBar',
    'SystemStartBrace',
    'SystemStartBracket',
    'SystemStartSquare',
    'TabNoteHead',
    'TextScript',
    'TextSpanner',
    'Tie',
    'TieColumn',
    'TimeSignature',
    'TrillPitchAccidental',
    'TrillPitchGroup',
    'TrillPitchHead',
    'TrillSpanner',
    'TupletBracket',
    'TupletNumber',
    'UnaCordaPedal',
    'UnaCordaPedalLineSpanner',
    'VaticanaLigature',
    'VerticalAlignment',
    'VerticalAxisGroup',
    'VoiceFollower',
    'VoltaBracket',
    'VoltaBracketSpanner',
)


DOUBLE_FLAT     = -1
THREE_Q_FLAT    = -0.75
FLAT            = -0.5
SEMI_FLAT       = -0.25
NATURAL         =  0
SEMI_SHARP      =  0.25
SHARP           =  0.5
THREE_Q_SHARP   =  0.75
DOUBLE_SHARP    =  1

pitchnames = {
    "nederlands": {
        "ceses": (0, DOUBLE_FLAT),
        "ceseh": (0, THREE_Q_FLAT),
        "ces": (0, FLAT),
        "ceh": (0, SEMI_FLAT),
        "c": (0, NATURAL),
        "cih": (0, SEMI_SHARP),
        "cis": (0, SHARP),
        "cisih": (0, THREE_Q_SHARP),
        "cisis": (0, DOUBLE_SHARP),

        "deses": (1, DOUBLE_FLAT),
        "deseh": (1, THREE_Q_FLAT),
        "des": (1, FLAT),
        "deh": (1, SEMI_FLAT),
        "d": (1, NATURAL),
        "dih": (1, SEMI_SHARP),
        "dis": (1, SHARP),
        "disih": (1, THREE_Q_SHARP),
        "disis": (1, DOUBLE_SHARP),

        "eeses": (2, DOUBLE_FLAT),
        "eses": (2, DOUBLE_FLAT),
        "eeseh": (2, THREE_Q_FLAT),
        "ees": (2, FLAT),
        "es": (2, FLAT),
        "eeh": (2, SEMI_FLAT),
        "e": (2, NATURAL),
        "eih": (2, SEMI_SHARP),
        "eis": (2, SHARP),
        "eisih": (2, THREE_Q_SHARP),
        "eisis": (2, DOUBLE_SHARP),

        "feses": (3, DOUBLE_FLAT),
        "feseh": (3, THREE_Q_FLAT),
        "fes": (3, FLAT),
        "feh": (3, SEMI_FLAT),
        "f": (3, NATURAL),
        "fih": (3, SEMI_SHARP),
        "fis": (3, SHARP),
        "fisih": (3, THREE_Q_SHARP),
        "fisis": (3, DOUBLE_SHARP),

        "geses": (4, DOUBLE_FLAT),
        "geseh": (4, THREE_Q_FLAT),
        "ges": (4, FLAT),
        "geh": (4, SEMI_FLAT),
        "g": (4, NATURAL),
        "gih": (4, SEMI_SHARP),
        "gis": (4, SHARP),
        "gisih": (4, THREE_Q_SHARP),
        "gisis": (4, DOUBLE_SHARP),

        "aeses": (5, DOUBLE_FLAT),
        "ases": (5, DOUBLE_FLAT),
        "aeseh": (5, THREE_Q_FLAT),
        "aes": (5, FLAT),
        "as": (5, FLAT),
        "aeh": (5, SEMI_FLAT),
        "a": (5, NATURAL),
        "aih": (5, SEMI_SHARP),
        "ais": (5, SHARP),
        "aisih": (5, THREE_Q_SHARP),
        "aisis": (5, DOUBLE_SHARP),

        "beses": (6, DOUBLE_FLAT),
        "beseh": (6, THREE_Q_FLAT),
        "bes": (6, FLAT),
        "beh": (6, SEMI_FLAT),
        "b": (6, NATURAL),
        "bih": (6, SEMI_SHARP),
        "bis": (6, SHARP),
        "bisih": (6, THREE_Q_SHARP),
        "bisis": (6, DOUBLE_SHARP),
    },
    "catalan": {
        "dobb": (0, DOUBLE_FLAT),
        "dob": (0, FLAT),
        "do": (0, NATURAL),
        "dod": (0, SHARP),
        "dodd": (0, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "reb": (1, FLAT),
        "re": (1, NATURAL),
        "red": (1, SHARP),
        "redd": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mib": (2, FLAT),
        "mi": (2, NATURAL),
        "mid": (2, SHARP),
        "midd": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fab": (3, FLAT),
        "fa": (3, NATURAL),
        "fad": (3, SHARP),
        "fadd": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "solb": (4, FLAT),
        "sol": (4, NATURAL),
        "sold": (4, SHARP),
        "soldd": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "lab": (5, FLAT),
        "la": (5, NATURAL),
        "lad": (5, SHARP),
        "ladd": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sib": (6, FLAT),
        "si": (6, NATURAL),
        "sid": (6, SHARP),
        "sidd": (6, DOUBLE_SHARP),

        # deprecated?
        "dos": (0, SHARP),
        "doss": (0, DOUBLE_SHARP),
        "res": (1, SHARP),
        "ress": (1, DOUBLE_SHARP),
        "mis": (2, SHARP),
        "miss": (2, DOUBLE_SHARP),
        "fas": (3, SHARP),
        "fass": (3, DOUBLE_SHARP),
        "sols": (4, SHARP),
        "solss": (4, DOUBLE_SHARP),
        "las": (5, SHARP),
        "lass": (5, DOUBLE_SHARP),
        "sis": (6, SHARP),
        "siss": (6, DOUBLE_SHARP),
    },
    "deutsch": {
        "ceses": (0, DOUBLE_FLAT),
        "ceseh": (0, THREE_Q_FLAT),
        "ces": (0, FLAT),
        "ceh": (0, SEMI_FLAT),
        "c": (0, NATURAL),
        "cih": (0, SEMI_SHARP),
        "cis": (0, SHARP),
        "cisih": (0, THREE_Q_SHARP),
        "cisis": (0, DOUBLE_SHARP),

        "deses": (1, DOUBLE_FLAT),
        "deseh": (1, THREE_Q_FLAT),
        "des": (1, FLAT),
        "deh": (1, SEMI_FLAT),
        "d": (1, NATURAL),
        "dih": (1, SEMI_SHARP),
        "dis": (1, SHARP),
        "disih": (1, THREE_Q_SHARP),
        "disis": (1, DOUBLE_SHARP),

        "eses": (2, DOUBLE_FLAT),
        "eseh": (2, THREE_Q_FLAT),
        "es": (2, FLAT),
        "eeh": (2, SEMI_FLAT), # should be eh; kept for backward compatibility
        "eh": (2, SEMI_FLAT),
        "e": (2, NATURAL),
        "eih": (2, SEMI_SHARP),
        "eis": (2, SHARP),
        "eisih": (2, THREE_Q_SHARP),
        "eisis": (2, DOUBLE_SHARP),

        "feses": (3, DOUBLE_FLAT),
        "feseh": (3, THREE_Q_FLAT),
        "fes": (3, FLAT),
        "feh": (3, SEMI_FLAT),
        "f": (3, NATURAL),
        "fih": (3, SEMI_SHARP),
        "fis": (3, SHARP),
        "fisih": (3, THREE_Q_SHARP),
        "fisis": (3, DOUBLE_SHARP),

        "geses": (4, DOUBLE_FLAT),
        "geseh": (4, THREE_Q_FLAT),
        "ges": (4, FLAT),
        "geh": (4, SEMI_FLAT),
        "g": (4, NATURAL),
        "gih": (4, SEMI_SHARP),
        "gis": (4, SHARP),
        "gisih": (4, THREE_Q_SHARP),
        "gisis": (4, DOUBLE_SHARP),

        "asas": (5, DOUBLE_FLAT),
        "ases": (5, DOUBLE_FLAT),   # non-standard name for asas
        "asah": (5, THREE_Q_FLAT),
        "aseh": (5, THREE_Q_FLAT),  # non-standard name for asah
        "as": (5, FLAT),
        "aeh": (5, SEMI_FLAT),  # should be ah; kepy for backward compatibility
        "ah": (5, SEMI_FLAT),
        "a": (5, NATURAL),
        "aih": (5, SEMI_SHARP),
        "ais": (5, SHARP),
        "aisih": (5, THREE_Q_SHARP),
        "aisis": (5, DOUBLE_SHARP),

        "heses": (6, DOUBLE_FLAT),
        "heseh": (6, THREE_Q_FLAT),
        "b": (6, FLAT),
        "beh": (6, SEMI_FLAT),
        "h": (6, NATURAL),
        "hih": (6, SEMI_SHARP),
        "his": (6, SHARP),
        "hisih": (6, THREE_Q_SHARP),
        "hisis": (6, DOUBLE_SHARP),
    },
    "english": {
        "cff": (0, DOUBLE_FLAT),
        "ctqf": (0, THREE_Q_FLAT),
        "cf": (0, FLAT),
        "cqf": (0, SEMI_FLAT),
        "c": (0, NATURAL),
        "cqs": (0, SEMI_SHARP),
        "cs": (0, SHARP),
        "ctqs": (0, THREE_Q_SHARP),
        "css": (0, DOUBLE_SHARP),
        "cx": (0, DOUBLE_SHARP),

        "dff": (1, DOUBLE_FLAT),
        "dtqf": (1, THREE_Q_FLAT),
        "df": (1, FLAT),
        "dqf": (1, SEMI_FLAT),
        "d": (1, NATURAL),
        "dqs": (1, SEMI_SHARP),
        "ds": (1, SHARP),
        "dtqs": (1, THREE_Q_SHARP),
        "dss": (1, DOUBLE_SHARP),
        "dx": (1, DOUBLE_SHARP),

        "eff": (2, DOUBLE_FLAT),
        "etqf": (2, THREE_Q_FLAT),
        "ef": (2, FLAT),
        "eqf": (2, SEMI_FLAT),
        "e": (2, NATURAL),
        "eqs": (2, SEMI_SHARP),
        "es": (2, SHARP),
        "etqs": (2, THREE_Q_SHARP),
        "ess": (2, DOUBLE_SHARP),
        "ex": (2, DOUBLE_SHARP),

        "fff": (3, DOUBLE_FLAT),
        "ftqf": (3, THREE_Q_FLAT),
        "ff": (3, FLAT),
        "fqf": (3, SEMI_FLAT),
        "f": (3, NATURAL),
        "fqs": (3, SEMI_SHARP),
        "fs": (3, SHARP),
        "ftqs": (3, THREE_Q_SHARP),
        "fss": (3, DOUBLE_SHARP),
        "fx": (3, DOUBLE_SHARP),

        "gff": (4, DOUBLE_FLAT),
        "gtqf": (4, THREE_Q_FLAT),
        "gf": (4, FLAT),
        "gqf": (4, SEMI_FLAT),
        "g": (4, NATURAL),
        "gqs": (4, SEMI_SHARP),
        "gs": (4, SHARP),
        "gtqs": (4, THREE_Q_SHARP),
        "gss": (4, DOUBLE_SHARP),
        "gx": (4, DOUBLE_SHARP),

        "aff": (5, DOUBLE_FLAT),
        "atqf": (5, THREE_Q_FLAT),
        "af": (5, FLAT),
        "aqf": (5, SEMI_FLAT),
        "a": (5, NATURAL),
        "aqs": (5, SEMI_SHARP),
        "as": (5, SHARP),
        "atqs": (5, THREE_Q_SHARP),
        "ass": (5, DOUBLE_SHARP),
        "ax": (5, DOUBLE_SHARP),

        "bff": (6, DOUBLE_FLAT),
        "btqf": (6, THREE_Q_FLAT),
        "bf": (6, FLAT),
        "bqf": (6, SEMI_FLAT),
        "b": (6, NATURAL),
        "bqs": (6, SEMI_SHARP),
        "bs": (6, SHARP),
        "btqs": (6, THREE_Q_SHARP),
        "bss": (6, DOUBLE_SHARP),
        "bx": (6, DOUBLE_SHARP),

        "c-flatflat": (0, DOUBLE_FLAT),
        "c-flat": (0, FLAT),
        "c-natural": (0, NATURAL),
        "c-sharp": (0, SHARP),
        "c-sharpsharp": (0, DOUBLE_SHARP),

        "d-flatflat": (1, DOUBLE_FLAT),
        "d-flat": (1, FLAT),
        "d-natural": (1, NATURAL),
        "d-sharp": (1, SHARP),
        "d-sharpsharp": (1, DOUBLE_SHARP),

        "e-flatflat": (2, DOUBLE_FLAT),
        "e-flat": (2, FLAT),
        "e-natural": (2, NATURAL),
        "e-sharp": (2, SHARP),
        "e-sharpsharp": (2, DOUBLE_SHARP),

        "f-flatflat": (3, DOUBLE_FLAT),
        "f-flat": (3, FLAT),
        "f-natural": (3, NATURAL),
        "f-sharp": (3, SHARP),
        "f-sharpsharp": (3, DOUBLE_SHARP),

        "g-flatflat": (4, DOUBLE_FLAT),
        "g-flat": (4, FLAT),
        "g-natural": (4, NATURAL),
        "g-sharp": (4, SHARP),
        "g-sharpsharp": (4, DOUBLE_SHARP),

        "a-flatflat": (5, DOUBLE_FLAT),
        "a-flat": (5, FLAT),
        "a-natural": (5, NATURAL),
        "a-sharp": (5, SHARP),
        "a-sharpsharp": (5, DOUBLE_SHARP),

        "b-flatflat": (6, DOUBLE_FLAT),
        "b-flat": (6, FLAT),
        "b-natural": (6, NATURAL),
        "b-sharp": (6, SHARP),
        "b-sharpsharp": (6, DOUBLE_SHARP),
    },
    "espanol": {
        "dobb": (0, DOUBLE_FLAT),
        "dotcb": (0, THREE_Q_FLAT),
        "dob": (0, FLAT),
        "docb": (0, SEMI_FLAT),
        "do": (0, NATURAL),
        "docs": (0, SEMI_SHARP),
        "dos": (0, SHARP),
        "dotcs": (0, THREE_Q_SHARP),
        "doss": (0, DOUBLE_SHARP),
        "dox": (0, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "retcb": (1, THREE_Q_FLAT),
        "reb": (1, FLAT),
        "recb": (1, SEMI_FLAT),
        "re": (1, NATURAL),
        "recs": (1, SEMI_SHARP),
        "res": (1, SHARP),
        "retcs": (1, THREE_Q_SHARP),
        "ress": (1, DOUBLE_SHARP),
        "rex": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mitcb": (2, THREE_Q_FLAT),
        "mib": (2, FLAT),
        "micb": (2, SEMI_FLAT),
        "mi": (2, NATURAL),
        "mics": (2, SEMI_SHARP),
        "mis": (2, SHARP),
        "mitcs": (2, THREE_Q_SHARP),
        "miss": (2, DOUBLE_SHARP),
        "mix": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fatcb": (3, THREE_Q_FLAT),
        "fab": (3, FLAT),
        "facb": (3, SEMI_FLAT),
        "fa": (3, NATURAL),
        "facs": (3, SEMI_SHARP),
        "fas": (3, SHARP),
        "fatcs": (3, THREE_Q_SHARP),
        "fass": (3, DOUBLE_SHARP),
        "fax": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "soltcb": (4, THREE_Q_FLAT),
        "solb": (4, FLAT),
        "solcb": (4, SEMI_FLAT),
        "sol": (4, NATURAL),
        "solcs": (4, SEMI_SHARP),
        "sols": (4, SHARP),
        "soltcs": (4, THREE_Q_SHARP),
        "solss": (4, DOUBLE_SHARP),
        "solx": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "latcb": (5, THREE_Q_FLAT),
        "lab": (5, FLAT),
        "lacb": (5, SEMI_FLAT),
        "la": (5, NATURAL),
        "lacs": (5, SEMI_SHARP),
        "las": (5, SHARP),
        "latcs": (5, THREE_Q_SHARP),
        "lass": (5, DOUBLE_SHARP),
        "lax": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sitcb": (6, THREE_Q_FLAT),
        "sib": (6, FLAT),
        "sicb": (6, SEMI_FLAT),
        "si": (6, NATURAL),
        "sics": (6, SEMI_SHARP),
        "sis": (6, SHARP),
        "sitcs": (6, THREE_Q_SHARP),
        "siss": (6, DOUBLE_SHARP),
        "six": (6, DOUBLE_SHARP),
    },
    "français": {
        "dobb": (0, DOUBLE_FLAT),
        "dobsb": (0, THREE_Q_FLAT),
        "dob": (0, FLAT),
        "dosb": (0, SEMI_FLAT),
        "do": (0, NATURAL),
        "dosd": (0, SEMI_SHARP),
        "dod": (0, SHARP),
        "dodsd": (0, THREE_Q_SHARP),
        "dodd": (0, DOUBLE_SHARP),
        "dox": (0, DOUBLE_SHARP),

        "rébb": (1, DOUBLE_FLAT),
        "rébsb": (1, THREE_Q_FLAT),
        "réb": (1, FLAT),
        "résb": (1, SEMI_FLAT),
        "ré": (1, NATURAL),
        "résd": (1, SEMI_SHARP),
        "réd": (1, SHARP),
        "rédsd": (1, THREE_Q_SHARP),
        "rédd": (1, DOUBLE_SHARP),
        "réx": (1, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "rebsb": (1, THREE_Q_FLAT),
        "reb": (1, FLAT),
        "resb": (1, SEMI_FLAT),
        "re": (1, NATURAL),
        "resd": (1, SEMI_SHARP),
        "red": (1, SHARP),
        "redsd": (1, THREE_Q_SHARP),
        "redd": (1, DOUBLE_SHARP),
        "rex": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mibsb": (2, THREE_Q_FLAT),
        "mib": (2, FLAT),
        "misb": (2, SEMI_FLAT),
        "mi": (2, NATURAL),
        "misd": (2, SEMI_SHARP),
        "mid": (2, SHARP),
        "midsd": (2, THREE_Q_SHARP),
        "midd": (2, DOUBLE_SHARP),
        "mix": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fabsb": (3, THREE_Q_FLAT),
        "fab": (3, FLAT),
        "fasb": (3, SEMI_FLAT),
        "fa": (3, NATURAL),
        "fasd": (3, SEMI_SHARP),
        "fad": (3, SHARP),
        "fadsd": (3, THREE_Q_SHARP),
        "fadd": (3, DOUBLE_SHARP),
        "fax": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "solbsb": (4, THREE_Q_FLAT),
        "solb": (4, FLAT),
        "solsb": (4, SEMI_FLAT),
        "sol": (4, NATURAL),
        "solsd": (4, SEMI_SHARP),
        "sold": (4, SHARP),
        "soldsd": (4, THREE_Q_SHARP),
        "soldd": (4, DOUBLE_SHARP),
        "solx": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "labsb": (5, THREE_Q_FLAT),
        "lab": (5, FLAT),
        "lasb": (5, SEMI_FLAT),
        "la": (5, NATURAL),
        "lasd": (5, SEMI_SHARP),
        "lad": (5, SHARP),
        "ladsd": (5, THREE_Q_SHARP),
        "ladd": (5, DOUBLE_SHARP),
        "lax": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sibsb": (6, THREE_Q_FLAT),
        "sib": (6, FLAT),
        "sisb": (6, SEMI_FLAT),
        "si": (6, NATURAL),
        "sisd": (6, SEMI_SHARP),
        "sid": (6, SHARP),
        "sidsd": (6, THREE_Q_SHARP),
        "sidd": (6, DOUBLE_SHARP),
        "six": (6, DOUBLE_SHARP),
    },
    "italiano": {
        "dobb": (0, DOUBLE_FLAT),
        "dobsb": (0, THREE_Q_FLAT),
        "dob": (0, FLAT),
        "dosb": (0, SEMI_FLAT),
        "do": (0, NATURAL),
        "dosd": (0, SEMI_SHARP),
        "dod": (0, SHARP),
        "dodsd": (0, THREE_Q_SHARP),
        "dodd": (0, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "rebsb": (1, THREE_Q_FLAT),
        "reb": (1, FLAT),
        "resb": (1, SEMI_FLAT),
        "re": (1, NATURAL),
        "resd": (1, SEMI_SHARP),
        "red": (1, SHARP),
        "redsd": (1, THREE_Q_SHARP),
        "redd": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mibsb": (2, THREE_Q_FLAT),
        "mib": (2, FLAT),
        "misb": (2, SEMI_FLAT),
        "mi": (2, NATURAL),
        "misd": (2, SEMI_SHARP),
        "mid": (2, SHARP),
        "midsd": (2, THREE_Q_SHARP),
        "midd": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fabsb": (3, THREE_Q_FLAT),
        "fab": (3, FLAT),
        "fasb": (3, SEMI_FLAT),
        "fa": (3, NATURAL),
        "fasd": (3, SEMI_SHARP),
        "fad": (3, SHARP),
        "fadsd": (3, THREE_Q_SHARP),
        "fadd": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "solbsb": (4, THREE_Q_FLAT),
        "solb": (4, FLAT),
        "solsb": (4, SEMI_FLAT),
        "sol": (4, NATURAL),
        "solsd": (4, SEMI_SHARP),
        "sold": (4, SHARP),
        "soldsd": (4, THREE_Q_SHARP),
        "soldd": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "labsb": (5, THREE_Q_FLAT),
        "lab": (5, FLAT),
        "lasb": (5, SEMI_FLAT),
        "la": (5, NATURAL),
        "lasd": (5, SEMI_SHARP),
        "lad": (5, SHARP),
        "ladsd": (5, THREE_Q_SHARP),
        "ladd": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sibsb": (6, THREE_Q_FLAT),
        "sib": (6, FLAT),
        "sisb": (6, SEMI_FLAT),
        "si": (6, NATURAL),
        "sisd": (6, SEMI_SHARP),
        "sid": (6, SHARP),
        "sidsd": (6, THREE_Q_SHARP),
        "sidd": (6, DOUBLE_SHARP),
    },
    "norsk": {
        "ceses": (0, DOUBLE_FLAT),
        "cessess": (0, DOUBLE_FLAT),
        "ces": (0, FLAT),
        "cess": (0, FLAT),
        "c": (0, NATURAL),
        "cis": (0, SHARP),
        "ciss": (0, SHARP),
        "cisis": (0, DOUBLE_SHARP),
        "cississ": (0, DOUBLE_SHARP),

        "deses": (1, DOUBLE_FLAT),
        "dessess": (1, DOUBLE_FLAT),
        "des": (1, FLAT),
        "dess": (1, FLAT),
        "d": (1, NATURAL),
        "dis": (1, SHARP),
        "diss": (1, SHARP),
        "disis": (1, DOUBLE_SHARP),
        "dississ": (1, DOUBLE_SHARP),

        "eeses": (2, DOUBLE_FLAT),
        "eessess": (2, DOUBLE_FLAT),
        "eses": (2, DOUBLE_FLAT),
        "essess": (2, DOUBLE_FLAT),
        "ees": (2, FLAT),
        "eess": (2, FLAT),
        "es": (2, FLAT),
        "ess": (2, FLAT),
        "e": (2, NATURAL),
        "eis": (2, SHARP),
        "eiss": (2, SHARP),
        "eisis": (2, DOUBLE_SHARP),
        "eississ": (2, DOUBLE_SHARP),

        "feses": (3, DOUBLE_FLAT),
        "fessess": (3, DOUBLE_FLAT),
        "fes": (3, FLAT),
        "fess": (3, FLAT),
        "f": (3, NATURAL),
        "fis": (3, SHARP),
        "fiss": (3, SHARP),
        "fisis": (3, DOUBLE_SHARP),
        "fississ": (3, DOUBLE_SHARP),

        "geses": (4, DOUBLE_FLAT),
        "gessess": (4, DOUBLE_FLAT),
        "ges": (4, FLAT),
        "gess": (4, FLAT),
        "g": (4, NATURAL),
        "g": (4, NATURAL),
        "gis": (4, SHARP),
        "giss": (4, SHARP),
        "gisis": (4, DOUBLE_SHARP),
        "gississ": (4, DOUBLE_SHARP),

        "aeses": (5, DOUBLE_FLAT),
        "aessess": (5, DOUBLE_FLAT),
        "ases": (5, DOUBLE_FLAT),
        "assess": (5, DOUBLE_FLAT),
        "aes": (5, FLAT),
        "aess": (5, FLAT),
        "as": (5, FLAT),
        "ass": (5, FLAT),
        "a": (5, NATURAL),
        "ais": (5, SHARP),
        "aiss": (5, SHARP),
        "aisis": (5, DOUBLE_SHARP),
        "aississ": (5, DOUBLE_SHARP),

        "bes": (6, DOUBLE_FLAT),
        "bess": (6, DOUBLE_FLAT),
        "b": (6, FLAT),
        "b": (6, FLAT),
        "h": (6, NATURAL),
        "his": (6, SHARP),
        "hiss": (6, SHARP),
        "hisis": (6, DOUBLE_SHARP),
        "hississ": (6, DOUBLE_SHARP),
    },
    "portugues": {
        "dobb": (0, DOUBLE_FLAT),
        "dobtqt": (0, THREE_Q_FLAT),
        "dob": (0, FLAT),
        "dobqt": (0, SEMI_FLAT),
        "do": (0, NATURAL),
        "dosqt": (0, SEMI_SHARP),
        "dos": (0, SHARP),
        "dostqt": (0, THREE_Q_SHARP),
        "doss": (0, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "rebtqt": (1, THREE_Q_FLAT),
        "reb": (1, FLAT),
        "rebqt": (1, SEMI_FLAT),
        "re": (1, NATURAL),
        "resqt": (1, SEMI_SHARP),
        "res": (1, SHARP),
        "restqt": (1, THREE_Q_SHARP),
        "ress": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mibtqt": (2, THREE_Q_FLAT),
        "mib": (2, FLAT),
        "mibqt": (2, SEMI_FLAT),
        "mi": (2, NATURAL),
        "misqt": (2, SEMI_SHARP),
        "mis": (2, SHARP),
        "mistqt": (2, THREE_Q_SHARP),
        "miss": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fabtqt": (3, THREE_Q_FLAT),
        "fab": (3, FLAT),
        "fabqt": (3, SEMI_FLAT),
        "fa": (3, NATURAL),
        "fasqt": (3, SEMI_SHARP),
        "fas": (3, SHARP),
        "fastqt": (3, THREE_Q_SHARP),
        "fass": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "solbtqt": (4, THREE_Q_FLAT),
        "solb": (4, FLAT),
        "solbqt": (4, SEMI_FLAT),
        "sol": (4, NATURAL),
        "solsqt": (4, SEMI_SHARP),
        "sols": (4, SHARP),
        "solstqt": (4, THREE_Q_SHARP),
        "solss": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "labtqt": (5, THREE_Q_FLAT),
        "lab": (5, FLAT),
        "labqt": (5, SEMI_FLAT),
        "la": (5, NATURAL),
        "lasqt": (5, SEMI_SHARP),
        "las": (5, SHARP),
        "lastqt": (5, THREE_Q_SHARP),
        "lass": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sibtqt": (6, THREE_Q_FLAT),
        "sib": (6, FLAT),
        "sibqt": (6, SEMI_FLAT),
        "si": (6, NATURAL),
        "sisqt": (6, SEMI_SHARP),
        "sis": (6, SHARP),
        "sistqt": (6, THREE_Q_SHARP),
        "siss": (6, DOUBLE_SHARP),
    },
    "suomi": {
        "ceses": (0, DOUBLE_FLAT),
        "ces": (0, FLAT),
        "c": (0, NATURAL),
        "cis": (0, SHARP),
        "cisis": (0, DOUBLE_SHARP),

        "deses": (1, DOUBLE_FLAT),
        "des": (1, FLAT),
        "d": (1, NATURAL),
        "dis": (1, SHARP),
        "disis": (1, DOUBLE_SHARP),

        "eses": (2, DOUBLE_FLAT),
        "es": (2, FLAT),
        "e": (2, NATURAL),
        "eis": (2, SHARP),
        "eisis": (2, DOUBLE_SHARP),

        "feses": (3, DOUBLE_FLAT),
        "fes": (3, FLAT),
        "f": (3, NATURAL),
        "fis": (3, SHARP),
        "fisis": (3, DOUBLE_SHARP),

        "geses": (4, DOUBLE_FLAT),
        "ges": (4, FLAT),
        "g": (4, NATURAL),
        "gis": (4, SHARP),
        "gisis": (4, DOUBLE_SHARP),

        "asas": (5, DOUBLE_FLAT),
        "ases": (5, DOUBLE_FLAT),   # non-standard name for asas
        "as": (5, FLAT),
        "a": (5, NATURAL),
        "ais": (5, SHARP),
        "aisis": (5, DOUBLE_SHARP),

        "bb": (6, DOUBLE_FLAT),    # should be bes; kept for backward compatibility
        "bes": (6, DOUBLE_FLAT),
        "heses": (6, DOUBLE_FLAT),  # non-standard name for bb
        "b": (6, FLAT),
        "h": (6, NATURAL),
        "his": (6, SHARP),
        "hisis": (6, DOUBLE_SHARP),
    },
    "svenska": {
        "cessess": (0, DOUBLE_FLAT),
        "cess": (0, FLAT),
        "c": (0, NATURAL),
        "ciss": (0, SHARP),
        "cississ": (0, DOUBLE_SHARP),

        "dessess": (1, DOUBLE_FLAT),
        "dess": (1, FLAT),
        "d": (1, NATURAL),
        "diss": (1, SHARP),
        "dississ": (1, DOUBLE_SHARP),

        "essess": (2, DOUBLE_FLAT),
        "ess": (2, FLAT),
        "e": (2, NATURAL),
        "eiss": (2, SHARP),
        "eississ": (2, DOUBLE_SHARP),

        "fessess": (3, DOUBLE_FLAT),
        "fess": (3, FLAT),
        "f": (3, NATURAL),
        "fiss": (3, SHARP),
        "fississ": (3, DOUBLE_SHARP),

        "gessess": (4, DOUBLE_FLAT),
        "gess": (4, FLAT),
        "g": (4, NATURAL),
        "giss": (4, SHARP),
        "gississ": (4, DOUBLE_SHARP),

        "assess": (5, DOUBLE_FLAT),
        "ass": (5, FLAT),
        "a": (5, NATURAL),
        "aiss": (5, SHARP),
        "aississ": (5, DOUBLE_SHARP),

        "hessess": (6, DOUBLE_FLAT),
        "b": (6, FLAT),
        "h": (6, NATURAL),
        "hiss": (6, SHARP),
        "hississ": (6, DOUBLE_SHARP),
    },
    "vlaams": {
        "dobb": (0, DOUBLE_FLAT),
        "dob": (0, FLAT),
        "do": (0, NATURAL),
        "dok": (0, SHARP),
        "dokk": (0, DOUBLE_SHARP),

        "rebb": (1, DOUBLE_FLAT),
        "reb": (1, FLAT),
        "re": (1, NATURAL),
        "rek": (1, SHARP),
        "rekk": (1, DOUBLE_SHARP),

        "mibb": (2, DOUBLE_FLAT),
        "mib": (2, FLAT),
        "mi": (2, NATURAL),
        "mik": (2, SHARP),
        "mikk": (2, DOUBLE_SHARP),

        "fabb": (3, DOUBLE_FLAT),
        "fab": (3, FLAT),
        "fa": (3, NATURAL),
        "fak": (3, SHARP),
        "fakk": (3, DOUBLE_SHARP),

        "solbb": (4, DOUBLE_FLAT),
        "solb": (4, FLAT),
        "sol": (4, NATURAL),
        "solk": (4, SHARP),
        "solkk": (4, DOUBLE_SHARP),

        "labb": (5, DOUBLE_FLAT),
        "lab": (5, FLAT),
        "la": (5, NATURAL),
        "lak": (5, SHARP),
        "lakk": (5, DOUBLE_SHARP),

        "sibb": (6, DOUBLE_FLAT),
        "sib": (6, FLAT),
        "si": (6, NATURAL),
        "sik": (6, SHARP),
        "sikk": (6, DOUBLE_SHARP),
    },
}
pitchnames["español"] = pitchnames["espanol"]
#pitchnames["francais"] = pitchnames["français"]

# a set with all the pitchnames for fast membership testing
all_pitchnames = frozenset(name for d in pitchnames.values() for name in d)

