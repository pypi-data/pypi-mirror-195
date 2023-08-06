import re

#original taken from https://github.com/pypa/packaging/blob/0238b79f7a3295084fb58de773d6822a10a1718a/packaging/version.py

class _BaseVersion(object):
    _key = None  # type: Union[CmpKey, LegacyCmpKey]

    def __hash__(self):
        # type: () -> int
        return hash(self._key)

    # Please keep the duplicated `isinstance` check
    # in the six comparisons hereunder
    # unless you find a way to avoid adding overhead function calls.
    def __lt__(self, other):
        # type: (_BaseVersion) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key < other._key

    def __le__(self, other):
        # type: (_BaseVersion) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key <= other._key

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key == other._key

    def __ge__(self, other):
        # type: (_BaseVersion) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key >= other._key

    def __gt__(self, other):
        # type: (_BaseVersion) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key > other._key

    def __ne__(self, other):
        # type: (object) -> bool
        if not isinstance(other, _BaseVersion):
            return NotImplemented

        return self._key != other._key

class LegacyVersion(_BaseVersion):
    def __init__(self, version):
        # type: (str) -> None
        self._version = str(version)
        self._key = _legacy_cmpkey(self._version)

        warnings.warn(
            "Creating a LegacyVersion has been deprecated and will be "
            "removed in the next major release",
            DeprecationWarning,
        )

    def __str__(self):
        # type: () -> str
        return self._version

    def __repr__(self):
        # type: () -> str
        return "<LegacyVersion({0})>".format(repr(str(self)))

    @property
    def public(self):
        # type: () -> str
        return self._version

    @property
    def base_version(self):
        # type: () -> str
        return self._version

    @property
    def epoch(self):
        # type: () -> int
        return -1

    @property
    def release(self):
        # type: () -> None
        return None

    @property
    def pre(self):
        # type: () -> None
        return None

    @property
    def post(self):
        # type: () -> None
        return None

    @property
    def dev(self):
        # type: () -> None
        return None

    @property
    def local(self):
        # type: () -> None
        return None

    @property
    def is_prerelease(self):
        # type: () -> bool
        return False

    @property
    def is_postrelease(self):
        # type: () -> bool
        return False

    @property
    def is_devrelease(self):
        # type: () -> bool
        return False


_legacy_version_component_re = re.compile(r"(\d+ | [a-z]+ | \.| -)", re.VERBOSE)

_legacy_version_replacement_map = {
    "pre": "c",
    "preview": "c",
    "-": "final-",
    "rc": "c",
    "dev": "@",
}


def _parse_version_parts(s):
    # type: (str) -> Iterator[str]
    for part in _legacy_version_component_re.split(s):
        part = _legacy_version_replacement_map.get(part, part)

        if not part or part == ".":
            continue

        if part[:1] in "0123456789":
            # pad for numeric comparison
            yield part.zfill(8)
        else:
            yield "*" + part

    # ensure that alpha/beta/candidate are before final
    yield "*final"


def _legacy_cmpkey(version):
    # type: (str) -> LegacyCmpKey

    # We hardcode an epoch of -1 here. A PEP 440 version can only have a epoch
    # greater than or equal to 0. This will effectively put the LegacyVersion,
    # which uses the defacto standard originally implemented by setuptools,
    # as before all PEP 440 versions.
    epoch = -1

    # This scheme is taken from pkg_resources.parse_version setuptools prior to
    # it's adoption of the packaging library.
    parts = []  # type: List[str]
    for part in _parse_version_parts(version.lower()):
        if part.startswith("*"):
            # remove "-" before a prerelease tag
            if part < "*final":
                while parts and parts[-1] == "*final-":
                    parts.pop()

            # remove trailing zeros from each series of numeric parts
            while parts and parts[-1] == "00000000":
                parts.pop()

        parts.append(part)

    return epoch, tuple(parts)


# Deliberately not anchored to the start and end of the string, to make it
# easier for 3rd party code to reuse
VERSION_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""