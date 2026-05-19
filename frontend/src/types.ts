export type AuthMode = "login" | "register";


export type User = {
  name: string;
  email: string;
};

export type Member = {
  name: string;
  age: number;
};

export type Group = {
  id: string;
  gymName: string;
  timeStart: string; // ISO string
  timeEnd: string;
  members: Member[];
};

export type Gym = {
  id: string;
  name: string;
  groups: Group[];
}