import glob
import os
import shutil
import unittest

from bilby.gw.prior import BBHPriorDict
from bilby_pipe import gracedb
from bilby_pipe.utils import BilbyPipeError

CERT_ALIAS = "X509_USER_PROXY"


class TestGraceDB(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.abspath(os.path.dirname(__file__))
        self.outdir = "outdir"
        self.example_gracedb_uid = "G298936"
        self.example_gracedb_uid_outdir = f"outdir_{self.example_gracedb_uid}"
        self.cert_dummy_path = os.path.join(self.directory, "temp/certdir/")
        self.tearDown()  # make sure that temp files deleted from previous attempts
        os.makedirs(self.cert_dummy_path)
        os.makedirs(self.outdir)

    def tearDown(self):
        if os.path.isdir(self.outdir):
            shutil.rmtree(self.outdir)
        if os.path.isdir(self.example_gracedb_uid_outdir):
            shutil.rmtree(self.example_gracedb_uid_outdir)
        if os.path.isdir(self.cert_dummy_path):
            shutil.rmtree(self.cert_dummy_path)

    def test_x509userproxy(self):
        """
        Tests if bilby_pipe.gracedb.x509userproxy(outdir)
        can move the user's CERT_ALIAS from the CERT_ALIAS dir to the outdir
        """
        # make temp cert file
        cert_alias_path = os.path.join(self.cert_dummy_path, CERT_ALIAS)
        temp_cert = open(cert_alias_path, "w")
        temp_cert.write("this is a test")
        temp_cert.close()

        # set os environ cert path
        os.environ[CERT_ALIAS] = cert_alias_path

        # get new cert path
        out = gracedb.x509userproxy(outdir=self.outdir)
        new_cert_path = os.path.join(self.outdir, "." + CERT_ALIAS)

        self.assertEqual(out, new_cert_path)

    def test_x509userproxy_no_cert(self):
        """
        No X509_USER_PROXY present, so gracedb.x509userprox is None
        """
        out = gracedb.x509userproxy(outdir=self.outdir)
        self.assertEqual(out, None)

    def test_x509userproxy_no_file(self):
        # set os environ cert path to path without cert
        os.environ.update({CERT_ALIAS: ""})

        out = gracedb.x509userproxy(outdir=self.outdir)
        self.assertEqual(out, None)

    # def test_read_from_gracedb(self):
    #    uid = "G298936"
    #    gracedb_url = 'https://gracedb.ligo.org/api/'
    #    gracedb.read_from_gracedb(uid, gracedb_url, self.outdir)

    def test_read_from_json(self):
        example_json_data = "examples/gracedb/G298936.json"
        out = gracedb.read_from_json(example_json_data)
        self.assertIsInstance(out, dict)

    def test_read_from_json_not_a_file(self):
        with self.assertRaises(FileNotFoundError):
            gracedb.read_from_json("not-a-file")

    # def test_create_config_file(self):
    #     example_json_data = "examples/gracedb/{}.json".format(self.example_gracedb_uid)
    #     candidate = gracedb.read_from_json(example_json_data)
    #     # Create ini file
    #     filename = gracedb.create_config_file(
    #         candidate, self.example_gracedb_uid, self.outdir
    #     )
    #     # Check it exists
    #     self.assertTrue(os.path.isfile(filename))
    #     # Read in using bilby_pipe
    #     parser = main.create_parser(top_level=True)
    #     args = parser.parse_args([filename])
    #     # Check it is set up correctly
    #     self.assertEqual(args.label, self.example_gracedb_uid)
    #     self.assertEqual(args.prior_file, "4s")

    # def test_create_config_file_roq(self):
    #     gracedb_uid = "G298936"
    #     example_json_data = "examples/gracedb/{}.json".format(gracedb_uid)
    #     candidate = gracedb.read_from_json(example_json_data)
    #     candidate["extra_attributes"]["CoincInspiral"]["mchirp"] = 2.1
    #     # Create ini file
    #     filename = gracedb.create_config_file(candidate, gracedb_uid, self.outdir)
    #     # Check it exists
    #     self.assertTrue(os.path.isfile(filename))
    #     # Read in using bilby_pipe
    #     parser = main.create_parser(top_level=True)
    #     args = parser.parse_args([filename])
    #     # Check it is set up correctly
    #     self.assertEqual(args.label, gracedb_uid)
    #     self.assertEqual(args.prior_file, "128s")
    #     self.assertEqual(args.likelihood_type, "ROQGravitationalWaveTransient")
    #     self.assertEqual(args.roq_folder, "/home/cbc/ROQ_data/IMRPhenomPv2/128s")

    def test_create_config_file_no_chirp_mass(self):
        gracedb_uid = "G298936"
        example_json_data = f"examples/gracedb/{gracedb_uid}.json"
        candidate = gracedb.read_from_json(example_json_data)
        channel_dict = dict(
            H1="GDS-CALIB_STRAIN_CLEAN",
            L1="GDS-CALIB_STRAIN_CLEAN",
            V1="Hrec_hoft_16384Hz",
        )
        webdir = "."
        sampler_kwargs = "{'a': 1, 'b': 2}"
        del candidate["extra_attributes"]["CoincInspiral"]["mchirp"]
        with self.assertRaises(BilbyPipeError):
            gracedb.create_config_file(
                candidate,
                gracedb_uid,
                channel_dict,
                self.outdir,
                sampler_kwargs,
                webdir,
            )

    def test_parse_args(self):
        example_json_data = f"examples/gracedb/{self.example_gracedb_uid}.json"
        parser = gracedb.create_parser()
        args = parser.parse_args(["--json", example_json_data])
        self.assertEqual(args.gracedb, None)
        self.assertEqual(args.json, example_json_data)
        self.assertEqual(args.output, "full")
        self.assertEqual(args.outdir, None)
        self.assertEqual(args.gracedb_url, "https://gracedb.ligo.org/api/")

    def test_create_prior_file_high_mass(self):
        gracedb.generate_cbc_prior_from_template(
            mode="phenompv2_bbh_roq",
            chirp_mass=20,
            likelihood_parameter_bounds=dict(
                chirp_mass_min=15,
                chirp_mass_max=45,
                mass_ratio_min=0.125,
                comp_min=10,
            ),
            outdir=self.outdir,
        )
        priors = BBHPriorDict(f"{self.outdir}/online.prior")
        self.assertEqual(priors["chirp_mass"].minimum, 15)
        self.assertEqual(priors["chirp_mass"].maximum, 45)
        self.assertEqual(priors["mass_ratio"].minimum, 0.125)
        self.assertEqual(priors["mass_1"].minimum, 10)

    def test_create_prior_file_low_mass(self):
        gracedb.generate_cbc_prior_from_template(
            mode="phenompv2_bbh_roq",
            chirp_mass=1.2,
            likelihood_parameter_bounds=dict(
                chirp_mass_min=1,
                chirp_mass_max=2,
                mass_ratio_min=0.125,
                comp_min=1,
            ),
            outdir=self.outdir,
        )
        priors = BBHPriorDict(f"{self.outdir}/online.prior")
        self.assertEqual(priors["chirp_mass"].minimum, 1.2 - 0.01)
        self.assertEqual(priors["chirp_mass"].maximum, 1.2 + 0.01)
        self.assertEqual(priors["mass_ratio"].minimum, 0.125)
        self.assertEqual(priors["mass_1"].minimum, 1)

    def test_main(self):
        gracedb_uid = "G298936"
        example_json_data = f"examples/gracedb/{gracedb_uid}.json"
        parser = gracedb.create_parser()
        args = parser.parse_args(
            ["--json", example_json_data, "--cbc-likelihood-mode", "test"]
        )
        gracedb.main(args)
        files = glob.glob(self.example_gracedb_uid_outdir + "/submit/*")
        print(files)
        # Check this creates all relevant jobs
        self.assertEqual(len(files), 9)


if __name__ == "__main__":
    unittest.main()
