# Elements of Distributed Computing
_written by Vijay K. Garg_

## Chapter 1

Distributed system, architecturally, passes messages to synchronize and share states. A global state only kind of exists. There are multiple processors that talk to each other by passing structured messages. Distributed system allow for commodity hardware to build powerful systems instead of using high-end specialized hardware to perform the same tasks.

A system is asyncronous if there is no upper bound between messages being passed between two processors. This means, in a system such as this, there is no perfectly possible way to differentiate between a slow processor and a failed processor.

No real way to synchronize clocks in a distributed system. Uncertainty in message delivery times. No easy way to sync clocks.


## Chapter 2

Set of events are generated when a program is executed, specifically a distributed program (beginning of a function, end of a function...). An ordering relation can be imposed upon a set of events. If a shared physical clock exists (and assuming all events are instantaneous and no two are simultaneous), then we ordering events is trivial,,, this is the _interleaving_ model of computation.

If there is no physical shared clock, having total order within a local processor is possible, however between processors, there is only a **partial** order. The order is set based on when information flow happens across processors, this is the _happened before_ model of computation.

The last kind of model is based on causality, instead of timings. Even if two events happen one after another on the same processor, they may not be causally related. There is no total ordering of events even within a single processor. This is the _potential causality_ model of computation.

A state is characterized by the value of all the variables including the program counter.

<hr>

Modelling a distributed system:
- loosely coupled
- message passing
- no shared memory
- no global clock

A distributed system consists of $N$ processes:
$\{P_1, P_2, ..., P_N\}$ and a set of unidirectional channels.

A channel connects two proceses. The state of the channel is defined by the sequence of messages sent across it (not received). 
It is assumed to have:
- infinite buffer
- error-free
> No assumption about ordering of messages  
> Messages have arbitrary but finite delay


Process is defined as a set of states, an initial condition ($\text{initial condition} \subset \text{states}$), and a set of events.

Each event may change the state of the process and the state of the channel (at most one) which is incident to _that_ process. 


<hr>

**Interleaving Model**

In this model of a distributed computation, a _run_ is a _global sequence of events_. All events in a run are interleaved.

> The **total order** is defined in the set of events. Refer to the bank example in textbook.

Here, the global state is the cross product of the local state of processes and the states of channels.  
An initial global state is where all the local states are in their initial conditions and all the channel states are empty.

> Processes record messages sent and received as part of their local state (advantageous to assume and happens in real life, too.)  
> Due to the assumption, the states of channels are determined via the recorded messages and there is no need to have the channel states within the cross prodcut to represent the global state. 

$\text{next(G, e)}$ gives the global state after event $e$ has occured.


$$ \text{G}_{i + 1} = \text{next(G}_i \text{, e}_i)\text{, for } 0 \leq i \leq m $$

> there are $m + 1$ global states and $G_0$ is the initial state.

<hr>

**Happened Before Model**

Leslie Lamport states that only a partial order can be determined between events. This model is more exacting to a true distributed system. 

> Events within a proccess are totally ordered.

Each process $P_i$ generates a sequence of local states and  events: $s_{i, 0}, e_{i, 0}, s_{i, 1}, ..., e_{i, l-1}, s_{i, l}$. The initial state of $P_i$ is $s_{i, 0}$. After $e_{i, j}$ is executed, the state of $P_i$ is $s_{i, j+1}$.

In process $P_i$: $e \prec_{im} f$ iff $e$ immediately precedes $f$ in the sequence of process in $P_i$.  
Therefore, $\text{next(e) = f}$ or $\text{prev(f) = e}$ whenever $e \prec_{im} f$.

> What is irreflexive transitive closure and reflexive transitive closure?

Event $e$ at $P_i$ _remotely precedes_ event $f$ at $P_j$ if $e$ is the send event of a message and $f$ is the receive event of that message. This is denoted by $e \leadsto f$.

The _happened before_ relation is denoted by $\rightarrow$.

_The happened before relation is the smallest relation that satisfies:_

$$(e \prec_{im} f)\ \vee \ (e \leadsto f)  \Rightarrow (e \rightarrow f),\ and$$
$$\exists g : (e \rightarrow g)\ \wedge \ (g \rightarrow f) \Rightarrow (e \rightarrow f).$$

A _run_ or _computation_ is denoted as a tuple $(E, \rightarrow)$ where $E$ is the set of events and $\rightarrow$ is a partial order on events $E$ such that all events within a single process are totally ordered (fulfulling the happened before model assumption). 

Event $e$ and $f$ are _concurrent_ (not related by the happened before relation) if $\neg (e \rightarrow f)$ $\wedge$ $\neg (f \rightarrow e)$.

Therefore,
$$ (e \parallel f) \equiv \neg (e \rightarrow f)\wedge \neg (f \rightarrow e)$$

<hr>

**Potential Causality Model**

We can accurately determine the order of events within a single process in any given system but we cannot be sure of the cause and effect of said events. Therefore, we are ascertaining that the events have been defined with a partial order as we are more concerned with the causality of events rather than the order of events.

_Causality relation_ (a partial order within a single process) is hard and expensive to determine, therefore, we use the _potential causality_ relations instead.

If an event $e$ causes event $f$ then event $e$ potentially causes event $f$. However, the converse is not true. Potential causality is a weaker relation than causality.

Definition of potential causality:

- $\text{If an event e potentially causes another event f on the same process then } e \xrightarrow{p} f$.
- $\text{If e is the send of a message and f is the corresponding receive, then } e \xrightarrow{p} f$.
- $\text{If } e \xrightarrow{p} f \text{ and } f \xrightarrow{p} g \text{, then } e \xrightarrow{p} g$

> $e$ and $f$ are _independent_ if $\neg (e \xrightarrow{p} f) \wedge \neg (f \xrightarrow{p} e)$

A potential causality diagram is a partially ordered set $(E, \xrightarrow{P})$ where $E$ is the set of events and $\xrightarrow{P}$ is the potential causality relation. $\xrightarrow{P}$ does not impose a total order within a process, unlike the _happened before_ relation.

> TODO: Understand the part below again  
When given a $(E, \xrightarrow{P})$ and a $(E, \rightarrow)$; the potential causality diagram is consistent with the happened before diagram if $ \xrightarrow{P} \ \subseteq \ \rightarrow $. 

A process wiht two threads might have both sets accessing mutually disjoint set of objects. In a happened before model, one access will happen after another, however the the previous access does not cause the latter access; here they aren't ordered.

<hr>

A distributed program can be viewed as a set of potential causality diagrams that it can generate. A potential causality diagram, in turn, is equivalent to a set of happened before diagrams. Each happened before diagram is equivalent to a set of global sequences of events (or states).

| **Model**           | **Basis**     | **Type**                             |
|---------------------|---------------|--------------------------------------|
| Interleaving        | Physical time | _Imposed_ total order on all events  |
| Happened before     | Logical time  | _Imposed_ total order on one process |
| Potential causality | Causality     | Partial order on a process           |



> Global sequence **cannot** be observed in the absence of a perfectly synchronized clock.  
> Multiple _happened before_ models can be consistent with one _potential causality_ model.

<hr>

Events and states are distinct things, events are the actions that change the state of a system.  
Another way to model distributed system is to model the computation as a sequence of states, instead of a sequence of events as we have been doing so far.

The difference between the two models is how one would draw the graph. In an events-based model, the nodes are the events itself, and a subset of the states (the ones being updated via the event) are in the channel (acting as the edge). Meanwhile, in a state-based model, the nodes are the states themselves, and the edges are the events that cause the state to change.

<hr>

> Every poset (partially ordered set) of events where the events in a process are totally ordered **is** a distributed computation.

_Not every_ poset of states is a valid distributed computation. The invalid poset of states are the ones that induce a cycle in the graph that describes the run/computation.

**Deposet** is a poset that does not have a cycle, at least in this case.

A deposet is a tuple $(S_1, ..., S_N, \leadsto)$ such that $(S, \rightarrow)$ is an irreflexive partial order that satisfies:

$$\forall i : \neg (\exists u : u \leadsto initial(i)) \text{ where } initial(i) \stackrel{\text{def}}{=} min\{S_i\}$$
$$\forall i : \neg (\exists u : final(i) \leadsto u)\text{ where } final(i) \stackrel{\text{def}}{=} max\{S_i\}$$
$$s \prec_{im} t \Rightarrow \neg (\exists u : s \leadsto u)\ \vee \ \neg (\exists u : u \leadsto t)$$

The above definition essentially says that there are no states before the initial state and no states after the final state. We cannot have multiple states simultaneously, this essentially means that an event either sends a message, or receives a message, or changes the internal state of the process but never more than one at a time.

A deposet or, more specifically, a _run_ of a distributed program defines a partial order on the set of states and events. Multiple total orders can exist within this partial order, a better way to state this is to say that many total orders are consistent with (or linearizations) of this partial order.  
A _global sequence_ is one such total order,,, one such linearization of a distributed computation.

A _global sequence_ is a sequence of _global states_ where a global state is just a vector of the linear states (refer to the definition upar, the cross product). 


$g$ is a global sequence of a run $r$ (denoted by $g \in linear(r)$) $\text{iff}$ the following holds:

$$\forall i : g \text{ restricted to } P_i = S_i$$
$$\forall k : g_k[i] \parallel g_k[j] \text{ where } g_k[i] \text{ is the state of } P_i \text{ in the global state } g_k$$
$$\forall k : g_k \text{ and } g_{k+1} \text{ differ in the state of exactly one process}$$

> $r = (S_1, ..., S_N, \leadsto)$ is $linear(r)$  
> $S_i$ is the sequence of local states in $P_i$  

The first constraint states that if an observer restricted themselves to a single process $P_i$, then they would observe $S_i$ or a _stutter_ of $S_i$. A _stutter_ is a finite repetition of $S_i$ .  
The second constraint requires that the local states that are part of the global state occur independently of each other (they don't have a causal relationship). This means that the states must be mutually pairwise concurrent.  
This constraint models the _interleaving_ assumption of events. Two events $e$ and $f$ cannot occur simultaneously. This is possible as events can either be send, receive or internal state change, therefore, only one process can change their states therefore in two consecutive global states, only one process can change their state.

<hr>

> Read page **24** of the textbook for the notation explanation.

<hr>

Problems



> The below is for the algorithm to find in the question 2.6  
> NOTE: leader election messaging algorithm


## Chapter 3

The interleaving model imposes a total order on all events, the imposition of the order can be achieved using a **logical clock**.  
The _happened before_ relation can be accurately tracked using a **vector clock**. A vector clock assigns timestamps to states (and events) such that the happened before relationship between states can be determined.

> A vector clock can be used to track potential causality as well, only if there is a mechnism in place to determine the independence of events with one another. This mechanism depends on the model of programming language being used.

> We are using state-based model of computation to talk about clocks, however, the same exact thing can be translated to an event-based model of computation.


If an accurately synchronized physical clock (a shared clock) exists then timestamping events using the clock would be sufficient to determine a total order.  
Logical clock is a way to determine an order that could have happened, one of the linearizations of a computation.

> Clocks in this case are only used to denote order, not the actually physical time that we are used to.

A logical clock $C$ is a map from $S$ to $\mathcal{N}$ (set of natural numbers) with the following constraint:

$$\forall s, t \in S : s \prec_{im} t \vee s \leadsto t \Rightarrow C(s) < C(t)$$

$C(s)$ for any $s \in S$ is that the process $s.p$ enters the state $s$ when the clock value is $C(s)$. 

Another constraint that is necessary for a logical clock that executation for each process is sequential in nature and message-passing takes a nonzero amount of time. This is equivalent to:

$$\forall s, t \in S : s \rightarrow t \Rightarrow \forall C \in \mathcal{C} : C(s) < C(t)$$

The above defined constraint is the definition of a _Lamport's Clock_.  
> $\mathcal{C}$ is the set of all possible logical clocks, and prove that it is a non-empty set. This can be shown if  $\rightarrow$ is an irreflixive partial order.

$$ \mathcal{C} \text{ is nonempty iff } (S, \rightarrow) \text{ is an irreflexive partial order.} $$

> The proof for the above lemma is on page 29 in the textbook.

Therefore, the converse of the definition is also true, $(S, \rightarrow)$ is not an irreflexive partial order if $\mathcal{C}$ is empty and no feasible clock exists.

This leads to the following lemma being true:

$$\forall u, v \in S : u \parallel v \Rightarrow \exists C \in \mathcal{C} : (C(u) = C(v))$$

The above states that if two states are concurrent then the clock will assign the same timestamp to both states. The above lemma also holds for any subset $X$ of $S$ which only contains pairwise concurrent states.

> The proof for the above is on page 30 in the textbook.

**Implementation**

A physical clock satisfies the definition of a logical clock, however, by definition, a distributed system does not have a shared physical clock.


```
P_i::
var
  c: integer      ;; initially 0

send event
  (s, send, t)    ;; s.c is sent as a part of the message
  t.c := s.c + 1

receive event
  (s, receive(u), t)
  t.c := max(s.c, u.c) + 1

internal event
  (s, internal, t)
  t.c := s.c + 1
```

In the above algorithm, `s` and `t` are states in process `P_i`. The events within the process change the state of the process from `s` to `t`. Within the receive event, the receive event is a message being sent by a process `P_j` where `i != j` and it is being sent by the state `u`.

We can verify the clock algorithm as:

$$\forall s, t \in S : s \rightarrow t \Rightarrow s.c < t.c$$

Some applications require all events in all process be totally ordered, we can easily do that by timestamping the events with the process identity and the clock value: $(s.c, s.p)$. The order can be obtained via:

$$(s.c, s.p) < (t.c, t.p) \stackrel{def}{=} (s.c < t.c)\ \vee \ ((s.c = t.c)\ \wedge \ (s.p < t.p))$$

The above just states that if the clock values are the same, then the process identity number is used to determine the order of the events.

**Vector Clocks**

The definition of a logical clock is not a biconditional. The converse of $\forall s, t : s \rightarrow t \Rightarrow s.c < t.c$ is not true. Logical clock lie in the domain of natural numbers, hence have a total ordering, unlike the computation $(S, \rightarrow)$ which is a partial order.

To take that into account, the definition of a vector clock is as follows:

$$ \forall s, t : s \rightarrow t \Leftrightarrow s.v < t.v $$

The comparison of vector clocks is as follows:

$$ x < y = (\forall k : 1 \leq k \leq N :\ x[k] \leq y[k]) \wedge (\exists j : 1 \leq j \leq N :\ x[k] < y[j]) $$
$$ x \leq y = (x < y) \vee (x = y) $$

**Implementation**

In this implementation, the vector is of size $N$, the number of processes in the system. A process increments its own component (index) in the vector clock. It's copy of the vector clock is sent in every outgoing message. 

```
P_j::

var
  v: array[1..N] of integer  ;; initially (∀i : i != j : v[i] = 0) ∧ (v[j] = 1)

send event
  (s, send, t)
  t.v := s.v
  t.v[j] := t.v[j] + 1

receive event
  (s, receive(u), t)
  for i := 1 to N, do
    t.v[i] := max(s.v[i], u.v[i])
  t.v[j] := t.v[j] + 1

internal event
  (s, internal, t)
  t.v := s.v
  t.v[j] := t.v[j] + 1
```

> The proof for why the above algorithm satsifies the vector clock definition is on page 36 in the textbook.


## Chapter 4

A variant of the vector clock algorithm, which preserves that happened before relationship between states, even if they are from difference processes.
The property it maintains is:

$$\forall s, t : s.p \neq t.p : s \rightarrow t \Leftrightarrow s.v < t.v$$

```
P_j::
  var
    v: array[1..N] of integer
      initially (∀i : i != j : v[i] = 0) ∧ (v[j] = 1);
    { initial(s) => (∀i : i != s.p : s.v[i] = 0) ∧ (s.v[s.p] = 1) }

  send event
  (s, send, t)
    t.v := s.v
    t.v[t.p] := t.v[t.p] + 1
  { (∀i : i != t.p : t.v[i] = s.v[i]) ∧ (t.v[t.p] > s.v[t.p]) }

  receive event
  (s, recv(u), t)
    for i := 1 to N, do
      t.v[i] := max(s.v[i], u.v[i])
  { (∀i : t.v[i] = max(s.v[i], u.v[i])) }  ;;???

  internal event
  (s, internal, t)
    t.v := s.v
  { t.v = s.v }
```

> A sample execution is in figure 4.2 on page 41 of the textbook.

**Induction is usually the prinicipal technique to verify distributed algorithms.**

