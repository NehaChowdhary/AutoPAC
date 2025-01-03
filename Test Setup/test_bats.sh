#!/usr/bin/env bats

load bats-support-clone
load test_helper/bats-support/load
load test_helper/redhatcop-bats-library/load

setup_file() {
  rm -rf /tmp/rhcop
  rm -f opa-profile.log
}

check_violations{
    {}
}

@test "check basic rego" {

  policy_dir=${1}
  policy_package=${2}
  schema_dir=${3}

  cmd="opa eval --input ${tmp}/list.yml --data policy/lib --data ${policy_dir}/src.rego --profile --format pretty --schema ${schema_dir} ${policy_package}"
  run ${cmd}

  print_info "${status}" "${output}" "${cmd}" "${tmp}"
  [ "$status" -eq 0 ]

  echo "${cmd} ${output}" >> opa-profile.log

  policy_id=$(check_violations "${tmp}/list.yml" "${policy_dir}" "${policy_package}")
  [ "${policy_id}" = "RHCOP-OCP_BESTPRACT-00001" ]
}