/*

Finish the specification of this notification concept,
including its events, scenarios, and operational principles.

*/ 
sig Resource {}

sig User {
	var reservations : set Resource
}

var sig Available in Resource {}

pred reserve[u : User, r : Resource] {
	// Make a reservation
	r in Available 
	
	Available' = Available - r 
	u.reservations' = u.reservations + r
}

pred cancel[u : User, r : Resource] {
	// Cancel a reservation
	r in u.reservations

	u.reservations' = u.reservations - r
	Available' = Available + r 
}

pred use[u : User, r : Resource] {
	// Use a reserved resource
	r in u.reservations

	Available' = Available 
	u.reservations' = u.reservations - r
}

pred cleanup {
	// Make all used resources available again
	some Resource - Available - User.reservations

	Available' = Resource - User.reservations
	reservations' = reservations
}

pred stutter {
	Available' = Available
	reservations' = reservations
}

fact {
	Available = Resource
	no reservations
	always {
		stutter
		or 
		cleanup
		or 
		(some u : User , r : Resource| reserve[u,r] or cancel[u,r] or use[u,r])
	}
}

// Validation

run Example {
	// Empty run to be used for simulation
}

run Scenario1 {
	// An user reserves a resource, uses it, and finally a cleanup occurs
	some u: User, r: Resource {
		reserve[u,r]; 
		use[u,r]; 
		cleanup
	}

} expect 1

run Scenario2 {
	// An user reserves a resource, cancels the reservation, and reserves again
	some u: User, r: Resource {
		reserve[u,r]; 
		cancel[u,r]; 
		reserve[u,r]
	}
} expect 1

run Scenario3 {
	// An user reserves two resources, cancels one, uses the other, and finally a cleanup occurs
	some u: User, r1: Resource, r2: Resource {
		reserve[u,r1]; 
		reserve[u,r2]; 
		cancel[u,r1]; 
              use[u,r2];
		cleanup
	}
} expect 1

run Scenario4 {
	// Two users try to reserve the same resource
	some u1: User, u2: User, r: Resource {
		reserve[u1,r]; 
		reserve[u2,r]
	}
} expect 0

run Scenario5 {
	// Eventually a cleanup is performed twice in a row
	 eventually(cleanup; cleanup)
} expect 0

// Verification

check OP1 {
	// Reserved resources aren't available
       all r: Resource | r in User.reservations implies r not in Available
}

check OP2 {
	// Used resources were reserved before
       all u: User, r: Resource | use[u,r] implies once reserve[u,r] //ter o once não obriga que a reserva seja feita imediatamente antes de usar o recurso

}

check OP3 {
	// Used resources can only be reserved again after a cleanup
       all u: User, r: Resource | use[u,r] 
       all u: User, r: Resource | use[u,r] implies cleanup
}

check OP4 {
	// After a cleanup all unreserved resources are available
	cleanup
	all r: Resource | r not in User.reservations and r in Available
}

check OP5 {
	// Cancel undoes reserve
	all u:User, r:Resource | always ((reserve[u,r]; cancel[u,r]) implies
		Available'' = Available and reservations'' = reservations)
}

check OP6 {
	// If a cleanup occurs some resource was used before
	always (cleanup implies once ( some u: User, r: Resource | use[u,r]))
}

check OP7 {
	// Used resources were not canceled since being reserved
	all u: User, r: Resource | always ( use[u, r] implies once reserve[u,r])
	all u: User, r: Resource | always ( use[u, r] implies (not cancel[u,r] since reserve[u,r]))
}

check OP8 {
	// Reserved resources can be used while not used or canceled
	all u: User, r: Resource | always reserve[u,r] implies
		 after (( use[u, r] or cancel[u,r]) releases r in u.reservations )
}

check OP9 {
	// The first event to occur will be a reservation
	always stutter or ( stutter until ( some u: User, r: Resource | reserved[u,r] ))
}

check OP10 {
	// If cleanups and cancels never occur the available resources keep diminishing
	always (not cleanup and all u: User, r: Resource | not cancel[u,r]) implies 
		always ( Available' in Available) 

}
