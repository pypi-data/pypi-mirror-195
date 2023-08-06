import copy
from typing import Optional

import networkx as nx
import numpy as np
import qiskit
import strangeworks
from strangeworks.core.errors.error import StrangeworksError

import strangeworks_qaoa.serializer as serializer
import strangeworks_qaoa.utils as utils


class StrangeworksQAOA:
    """Strangeworks client object."""

    def __init__(self, resource_slug: Optional[str] = " ") -> None:
        if resource_slug != " " and resource_slug != "":
            self.rsc = strangeworks.resources(slug=resource_slug)[0]
        else:
            rsc_list = strangeworks.resources()
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == "qaoa":
                    self.rsc = rsc_list[rr]

        self.backend_list = " "

    def backends(self):
        """
        To-Do: Add cross check as to which backends the current user actually has access to.
                Currently, this just lists all backends that could work with the qaoa service.
        """

        all_backends = strangeworks.backends(backend_type_slugs=["sw-qaoa"])

        aws_backends = []
        aws_sim_backends = []
        ibmq_backends = []
        ibm_cloud_backends = []
        ibm_sim_backends = []
        for bb in range(len(all_backends)):
            try:
                arn_str = all_backends[bb].remote_backend_id[0:3]
                # print(arn_str)
                if arn_str == "arn" and all_backends[bb].remote_status != "retired":
                    if (
                        all_backends[bb].name == "SV1"
                        or all_backends[bb].name == "TN1"
                        or all_backends[bb].name == "dm1"
                    ):
                        backend_temp = {
                            "name": all_backends[bb].name,
                            "provider": "AWS_Simulator",
                            "remote_status": all_backends[bb].remote_status,
                            "arn": all_backends[bb].remote_backend_id,
                        }
                        aws_sim_backends.append(backend_temp)
                    else:
                        backend_temp = {
                            "name": all_backends[bb].name,
                            "provider": "AWS",
                            "remote_status": all_backends[bb].remote_status,
                            "arn": all_backends[bb].remote_backend_id,
                        }
                        aws_backends.append(backend_temp)
            except:
                None

            try:
                ibm_str = all_backends[bb].name[0:3]
                id_str = all_backends[bb].remote_backend_id[0:3]
                if ibm_str == "ibm":
                    if id_str == "ibm":
                        prov = "IBM_Cloud"
                        backend_temp = {
                            "backend_name": all_backends[bb].name,
                            "provider": prov,
                            "remote_status": all_backends[bb].remote_status,
                        }
                        ibm_cloud_backends.append(backend_temp)
                    else:
                        if all_backends[bb].name == "ibmq_qasm_simulator":
                            prov = "IBM_Simulator"
                            backend_temp = {
                                "backend_name": all_backends[bb].name,
                                "provider": prov,
                                "remote_status": all_backends[bb].remote_status,
                            }
                            ibm_sim_backends.append(backend_temp)
                        else:
                            prov = "IBMQ"
                            backend_temp = {
                                "backend_name": all_backends[bb].name,
                                "provider": prov,
                                "remote_status": all_backends[bb].remote_status,
                            }
                            ibmq_backends.append(backend_temp)
                elif ibm_str == "sim":
                    prov = "IBM_Simulator"
                    backend_temp = {
                        "backend_name": all_backends[bb].name,
                        "provider": prov,
                        "remote_status": all_backends[bb].remote_status,
                    }
                    ibm_sim_backends.append(backend_temp)
            except:
                None

        self.backend_list = {
            "AWS": aws_backends,
            "AWS_Sim": aws_sim_backends,
            "IBMQ": ibmq_backends,
            "IBM_Cloud": ibm_cloud_backends,
            "IBM_Sim": ibm_sim_backends,
        }

        return self.backend_list

    def run(self, backend, problem, problem_params):
        if self.backend_list == " ":
            self.backends()

        aws = False
        ibm = False
        for nn in range(len(self.backend_list["AWS"])):
            if self.backend_list["AWS"][nn]["name"] == backend:
                aws = True
                backend_id = self.backend_list["AWS"][nn]["arn"]

        for nn in range(len(self.backend_list["IBMQ"])):
            if self.backend_list["IBMQ"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_quantum"
                backend_id = self.backend_list["IBMQ"][nn]["backend_name"]

        for nn in range(len(self.backend_list["IBM_Cloud"])):
            if self.backend_list["IBM_Cloud"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_cloud"
                backend_id = self.backend_list["IBM_Cloud"][nn]["backend_name"]

        for nn in range(len(self.backend_list["AWS_Sim"])):
            if self.backend_list["AWS_Sim"][nn]["name"] == backend:
                aws = True
                backend_id = self.backend_list["AWS_Sim"][nn]["arn"]

        for nn in range(len(self.backend_list["IBM_Sim"])):
            if self.backend_list["IBM_Sim"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_quantum"
                backend_id = self.backend_list["IBM_Sim"][nn]["backend_name"]

        if ibm is False and aws is False:
            Exception()

        # Check which format the problem is specified in and convert to the form which our QUBO solver can accept.
        if type(problem) == nx.classes.graph.Graph:
            H = utils.get_Ham_from_graph(problem)
        elif type(problem) == qiskit.opflow.primitive_ops.pauli_sum_op.PauliSumOp:
            H = utils.get_Ham_from_PauliSumOp(problem)
        elif type(problem) == np.ndarray:
            H = utils.get_Ham_from_QUBO(problem)

        shotsin = problem_params["shotsin"]
        maxiter = problem_params["maxiter"]
        try:
            problem_type = problem_params["problem_type"]
        except:
            problem_type = "Classical"
        try:
            p = problem_params["p"]
        except:
            x = None
        try:
            theta0 = problem_params["theta0"]
        except:
            x = None
        try:
            optimizer = problem_params["optimizer"]
        except:
            x = None
        try:
            ansatz = problem_params["ansatz"]
        except:
            x = None

        hyperparams = {
            "H": serializer.pickle_serializer(H, "json"),
            "theta0": str(theta0),
            "nqubits": str(len(H[0][1])),
            "p": str(p),
            "maxiter": str(maxiter),
            "optimizer": optimizer,
            "shotsin": str(shotsin),
            "ansatz": ansatz,
            "problem_type": problem_type,
        }

        if aws is True:
            input_params = {
                "provider": "aws",
                "dev_str": backend_id,
                "hyperparams": hyperparams,
            }
        elif ibm is True:
            input_params = {
                "provider": "ibm",
                "channel": channel,
                "backend": backend_id,
                "hyperparams": hyperparams,
            }

        input_json = serializer.pickle_serializer(input_params, "json")
        input_json = {"payload": input_json}

        sw_job = strangeworks.execute(self.rsc, input_json, "run_hybrid_job")

        return sw_job

    def update_status(self, sw_job):
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        status = strangeworks.execute(
            self.rsc, {"payload": {"job_slug": job_slug}}, "status"
        )

        return status

    def get_results(self, sw_job, calculate_exact_sol=False, display_results=False):
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        result_url = strangeworks.execute(
            self.rsc, {"payload": {"job_slug": job_slug}}, "get_results_url"
        )

        if result_url:
            result_file = strangeworks.download_job_files([result_url])[0]
        else:
            """
            If results file is not there, run the function to produce the results file
            and plots for the platform
            """
            result = strangeworks.execute(
                self.rsc, {"payload": {"job_slug": job_slug}}, "result"
            )

            result = serializer.pickle_deserializer(result, "json")

            if result.strip().upper() == "COMPLETED":
                result_url = strangeworks.execute(
                    self.rsc, {"payload": {"job_slug": job_slug}}, "get_results_url"
                )
                if result_url:
                    result_file = strangeworks.download_job_files([result_url])
                else:
                    raise StrangeworksError(f"unable to open {result_url}")
            else:
                return result

        if calculate_exact_sol:
            inputs_url = strangeworks.execute(
                self.rsc, {"payload": {"job_slug": job_slug}}, "get_inputs_url"
            )
            inputs = strangeworks.download_job_files([inputs_url])[0]

            H = serializer.pickle_deserializer(inputs["H"], "json")

            try:
                # En_exact = utils.get_exact_en(utils.get_PauliSumOp_from_Ham(H), len(H[0][1]))
                En_exact = utils.get_exact_en(utils.get_graph_from_Ham(H), len(H[0][1]))
            except:
                En_exact = "!!problem too big for exact solution!!"
            result_file["En_exact"] = En_exact
        else:
            result_file["En_exact"] = None

        if display_results:
            sol = result_file["sol"]
            En_exact = result_file["En_exact"]
            En_sol = result_file["en_min"]
            En_av = result_file["en"][len(result_file["en"]) - 1]

            print(
                f"The average energy (expectation value) of the final state is {En_av}"
            )
            print(f"The solution found by the algorithm is: {sol}")
            print(f"The energy of the solution found by the algorithm is {En_sol}")
            print(f"The exact optimal energy is {En_exact}")

        return result_file

    def job_list(self, update_status=True):
        job_list = strangeworks.jobs()

        qaoa_job_list = []
        for jj in range(len(job_list)):
            if job_list[jj].resource.product.slug == "qaoa":
                if job_list[jj].external_identifier[0:3] == "arn":
                    prov = "AWS"
                else:
                    prov = "IBM"

                if job_list[jj].status != "COMPLETED" and update_status is True:
                    try:
                        status = strangeworks.execute(
                            self.rsc,
                            {"payload": {"job_slug": job_list[jj].slug}},
                            "status",
                        )
                    except:
                        status = job_list[jj].status
                else:
                    status = job_list[jj].status

                temp = {
                    "slug": job_list[jj].slug,
                    "Status": status,
                    "Provider": prov,
                    "resource_slug": job_list[jj].resource.slug,
                }
                qaoa_job_list.append(temp)

        return qaoa_job_list

    # def jobs(self, slug):

    #     sw_job = strangeworks.jobs(slug=slug)[0]

    #     return QAOAJob()
