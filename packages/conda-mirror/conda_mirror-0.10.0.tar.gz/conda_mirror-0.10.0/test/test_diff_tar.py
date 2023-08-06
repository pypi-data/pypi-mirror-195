import json
import os
import pathlib
import shutil
import sys
import tempfile
from os.path import isfile, join

import pytest

import conda_mirror.diff_tar as dt

EMPTY_MD5 = "d41d8cd98f00b204e9800998ecf8427e"


@pytest.fixture
def tmpdir():
    tmpdir = tempfile.mkdtemp()
    dt.mirror_dir = join(tmpdir, "repo")
    dt.DEFAULT_REFERENCE_PATH = join(tmpdir, "reference.json")
    dt.DEFAULT_UPDATE_PATH = join(tmpdir, "updates.tar")
    yield tmpdir
    shutil.rmtree(tmpdir)


def test_md5_file(tmpdir):
    tmpfile = join(tmpdir, "testfile")
    with open(tmpfile, "wb") as fo:
        fo.write(b"A\n")
    assert dt.md5_file(tmpfile) == "bf072e9119077b4e76437a93986787ef"


def create_test_repo(subdirname="linux-64"):
    subdir = join(dt.mirror_dir, subdirname)
    os.makedirs(subdir)
    with open(join(subdir, "repodata.json"), "w") as fo:
        fo.write(json.dumps({"packages": {"a-1.0-0.tar.bz2": {"md5": EMPTY_MD5}}}))
    for fn in "repodata.json.bz2", "a-1.0-0.tar.bz2":
        with open(join(subdir, fn), "wb") as fo:
            pass


def test_find_repos(tmpdir):
    create_test_repo()
    assert list(dt.find_repos(dt.mirror_dir)) == [join(dt.mirror_dir, "linux-64")]


def test_all_repodata_repos(tmpdir):
    create_test_repo()
    d = dt.all_repodata(dt.mirror_dir)
    assert d[join(dt.mirror_dir, "linux-64")]["a-1.0-0.tar.bz2"]["md5"] == EMPTY_MD5


def test_verify_all_repos(tmpdir):
    create_test_repo()
    dt.verify_all_repos(dt.mirror_dir)


def test_read_no_reference(tmpdir):
    # tmpdir is empty - join(tmpdir, 'reference.json') does not exist
    with pytest.raises(dt.NoReferenceError):
        dt.read_reference()


def test_write_and_read_reference(tmpdir):
    create_test_repo()
    dt.write_reference(join(tmpdir, "repo"))
    ref = dt.read_reference()
    assert ref[join(dt.mirror_dir, "linux-64")]["a-1.0-0.tar.bz2"]["md5"] == EMPTY_MD5


def test_write_and_read_reference_with_target(tmpdir):
    create_test_repo()
    dt.write_reference(join(tmpdir, "repo"), join(tmpdir, "reference_target.json"))
    ref = dt.read_reference(join(tmpdir, "reference_target.json"))
    assert ref[join(dt.mirror_dir, "linux-64")]["a-1.0-0.tar.bz2"]["md5"] == EMPTY_MD5


def test_get_updates(tmpdir):
    create_test_repo()
    dt.write_reference(join(tmpdir, "repo"))
    assert list(dt.get_updates(dt.mirror_dir)) == []

    create_test_repo("win-32")
    lst = sorted(pathlib.Path(f) for f in dt.get_updates(dt.mirror_dir))
    assert lst == [
        pathlib.Path("win-32/a-1.0-0.tar.bz2"),
        pathlib.Path("win-32/repodata.json"),
        pathlib.Path("win-32/repodata.json.bz2"),
    ]


def test_get_updates_with_target(tmpdir):
    create_test_repo()
    dt.write_reference(join(tmpdir, "repo"), join(tmpdir, "reference_target.json"))
    assert (
        list(dt.get_updates(dt.mirror_dir, join(tmpdir, "reference_target.json"))) == []
    )

    create_test_repo("win-32")
    lst = sorted(
        pathlib.Path(f)
        for f in dt.get_updates(dt.mirror_dir, join(tmpdir, "reference_target.json"))
    )
    assert lst == [
        pathlib.Path("win-32/a-1.0-0.tar.bz2"),
        pathlib.Path("win-32/repodata.json"),
        pathlib.Path("win-32/repodata.json.bz2"),
    ]


def test_tar_repo(tmpdir):
    create_test_repo()
    dt.write_reference(dt.mirror_dir)
    create_test_repo("win-32")
    dt.tar_repo(dt.mirror_dir)
    assert isfile(dt.DEFAULT_UPDATE_PATH)


def test_tar_repo_with_target(tmpdir):
    create_test_repo()
    tarball = join(tmpdir, "updates_target.tar")
    reference = join(tmpdir, "reference_target.json")
    dt.write_reference(dt.mirror_dir, reference)
    create_test_repo("win-32")
    dt.tar_repo(dt.mirror_dir, reference, tarball)
    assert isfile(tarball)


def run_with_args(args):
    old_args = list(sys.argv)
    sys.argv = ["conda-diff-tar"] + args
    dt.main()
    sys.argv = old_args


def test_version():
    run_with_args(["--version"])


def test_cli_reference(tmpdir):
    create_test_repo()
    run_with_args(["--reference", dt.mirror_dir])
    assert isfile(dt.DEFAULT_REFERENCE_PATH)


def test_cli_reference_outfile(tmpdir):
    target_path = join(tmpdir, "ref_target.json")
    create_test_repo()
    run_with_args(["--reference", dt.mirror_dir])
    assert isfile(dt.DEFAULT_REFERENCE_PATH)
    run_with_args(["--reference", "--outfile", target_path, dt.mirror_dir])
    assert isfile(target_path)
    with open(dt.DEFAULT_REFERENCE_PATH) as ref1:
        with open(target_path) as ref2:
            assert ref1.readlines() == ref2.readlines()


def test_cli_create_outfile(tmpdir):
    target_path = join(tmpdir, "tar_target.tar")
    create_test_repo()
    run_with_args(["--reference", dt.mirror_dir])
    run_with_args(["--create", "--outfile", target_path, dt.mirror_dir])
    assert isfile(target_path)


def test_cli_create_infile(tmpdir):
    target_ref_path = join(tmpdir, "ref_target.json")
    create_test_repo()
    run_with_args(["--reference", "--outfile", target_ref_path, dt.mirror_dir])
    assert isfile(target_ref_path)
    run_with_args(["--create", "--infile", target_ref_path, dt.mirror_dir])
    assert isfile(dt.DEFAULT_UPDATE_PATH)


def test_cli_create_infile_outfile(tmpdir):
    target_tar_path = join(tmpdir, "tar_target.tar")
    target_ref_path = join(tmpdir, "ref_target.json")
    create_test_repo()
    run_with_args(["--reference", "--outfile", target_ref_path, dt.mirror_dir])
    assert isfile(target_ref_path)
    run_with_args(
        [
            "--create",
            "--outfile",
            target_tar_path,
            "--infile",
            target_ref_path,
            dt.mirror_dir,
        ]
    )
    assert isfile(target_tar_path)


def test_misc(tmpdir):
    create_test_repo()
    run_with_args(["--reference", dt.mirror_dir])
    create_test_repo("win-32")
    run_with_args(["--show", dt.mirror_dir])
    run_with_args(["--create", "--verbose", dt.mirror_dir])
    run_with_args(["--verify", dt.mirror_dir])
    run_with_args([dt.mirror_dir])  # do nothing
