import collections.abc
import typing

from mercurial import (
    hg,
    localrepo,
    ui,
    util as hgutil,
)

MAP_FILE_NAME = b"git-mapfile"


def get_repo_and_gitdir(repo):
    if repo.shared():
        repo = hg.sharedreposource(repo)

    if repo.ui.configbool(b"git", b"intree"):
        gitdir = repo.wvfs.join(b".git")
    else:
        gitdir = repo.vfs.join(b"git")

    return repo, gitdir


class State(collections.abc.Mapping):
    def __init__(self, ui, repo):
        super().__init__()

        self.ui = ui
        self.store_repo, self.gitdir = get_repo_and_gitdir(repo)
        self.vfs = self.store_repo.vfs

    def __bool__(self):
        return bool(self.__oneway_map)

    @hgutil.propertycache
    def __onewaymap(self):
        return dict(self.load(ui, repo))

    @hgutil.propertycache
    def __twowaymap(self):
        r = self.__onewaymap.copy()
        r.update(map(reversed, r.items()))

        return r

    def __getitem__(self, item):
        return self.__twoway_map[item]

    def set(self, gitsha, hgsha):
        self.__oneway_map[gitsha] = hgsha
        self.__twoway_map[gitsha] = hgsha
        self.__twoway_map[hgsha] = gitsha

    def __getitem__(self, item):
        return self.__twoway_map[item]

    def __iter__(self):
        return iter(self.__oneway_map)

    def __len__(self):
        return len(self.__oneway_map)

    @abc.abstractmethod
    def load(self) -> typing.Iterator[(bytes, bytes)]:
        pass

    @abc.abstractmethod
    def save(self, tr) -> typing.Iterator[(bytes, bytes)]:
        pass


class LegacyState(AbstractState):
    def load(self):
        if os.path.exists(self.vfs.join(self.map_file)):
            for line in self.vfs(self.map_file):
                # format is <40 hex digits> <40 hex digits>\n
                if len(line) != 82:
                    raise ValueError(
                        _(b"corrupt mapfile: incorrect line length %d")
                        % len(line)
                    )
                yield line[:40], line[41:81]
                map_git_real[gitsha] = hgsha
                map_hg_real[hgsha] = gitsha
        self._map_git_real = map_git_real
        self._map_hg_real = map_hg_real
