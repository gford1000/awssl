import awssl

def parallel_example():

	# Construct states for each branch 
	branch1 = awssl.Wait(
		Name="Wait 20s",
		WaitForSeconds=20,
		EndState=True)

	wait_10s = awssl.Wait(
		Name="Wait 10s",
		WaitForSeconds=10,
		EndState=True)

	branch2 = awssl.Pass(
		Name="Pass",
		NextState=wait_10s)

	# Construct states for main branch
	final_state = awssl.Pass(
		Name="Final State",
		EndState=True)

	parallel = awssl.Parallel(
		Name="Parallel",
		NextState=final_state,
		EndState=False,
		BranchList=[branch1, branch2])

	# Construct state machine
	return awssl.StateMachine(
		Comment="An example of the Amazon States Language using a parallel state to execute two branches at the same time.",
		StartState=parallel)

if __name__ == "__main__":
	sm = parallel_example()
	print sm

