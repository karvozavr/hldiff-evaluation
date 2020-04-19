import os
from shutil import copyfile
import logging

import click
from pydriller import RepositoryMining, ModificationType, GitRepository, Modification


def java_file_filter(filename: str):
    return filename.endswith('.java')


def save(repo, commit, filename, before, after):
    path = os.path.join('filepairs', repo, commit)
    os.makedirs(path)
    before_saved = os.path.join(path, 'before__' + filename)
    after_saved = os.path.join(path, 'after__' + filename)
    copyfile(before, before_saved)
    copyfile(after, after_saved)


class RepositoryProcessor:

    def __init__(self, repository: str):
        self.repository = repository
        self.repo = GitRepository(repository)
        self.mining = RepositoryMining(repository)
        self.pairs = []

    def get_all_filepairs(self, file_filter=java_file_filter):
        commits = list(filter(lambda x: not x.merge, self.mining.traverse_commits()))
        for commit in commits:
            logging.log(logging.INFO, f'Processing commit {commit.hash}')
            for modification in commit.modifications:
                if modification.change_type == ModificationType.MODIFY:
                    if file_filter(modification.filename):
                        self.get_file_pair(commit, modification)

    def get_file_pair(self, commit, modification: Modification):
        parent = commit.parents[0]

        repo = self.repo.project_name
        commit_hash = commit.hash
        filename = modification.filename

        path = os.path.join('filepairs', repo, commit_hash, filename)
        os.makedirs(path, exist_ok=True)

        self.repo.checkout(parent)
        before = os.path.join(self.repository, modification.old_path)
        before_saved = os.path.join(path, 'before_' + commit_hash + '_' + filename)
        logging.log(logging.ERROR, before_saved)
        copyfile(before, before_saved)

        self.repo.checkout(commit_hash)
        after = os.path.join(self.repository, modification.new_path)
        after_saved = os.path.join(path, 'after__' + commit_hash + '_' + filename)
        copyfile(after, after_saved)

        self.pairs.append((before_saved, after_saved))


@click.command()
@click.argument('repository')
def filepairs(repository):
    processor = RepositoryProcessor(repository)
    processor.get_all_filepairs()
    pairs = processor.pairs
    with open('filepairs/pairs.txt', 'w') as f:
        f.write('\n'.join(map(lambda x: f'{x[0]} {x[1]}', pairs)))


if __name__ == '__main__':
    filepairs()
