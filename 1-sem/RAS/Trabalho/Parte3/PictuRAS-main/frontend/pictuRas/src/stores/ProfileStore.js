import { defineStore } from 'pinia';
import axios from 'axios';

const api = import.meta.env.VITE_API_GATEWAY;

export const useProfileStore = defineStore('profileStore', {
    state: () => ({
        profile: {},
        completeProfile: {},
        loading: false,
        error: null,
        userPlanName: null,
    }),

    actions: {
        async fetchProfile() {
            this.loading = true;
            this.error = null;
            
            try {
                const response = await axios.get(`${api}/api/profile`,{ withCredentials: true } );
                this.profile = response.data;
                const planId = this.profile.plan;
                const responsePlan = await axios.get(`${api}/api/plan/${planId}`, {
                    withCredentials: true  
                });
                this.userPlanName = responsePlan.data.name;
                this.profile.plan = this.userPlanName;
            }
            catch (error) {
                this.error = `Failed to fetch profile for user ID: ${this.profile.email}`;
            }
            finally {
                this.loading = false;
            }
        },

        async updateProfile(updatedProfile) {
            this.loading = true;
            this.error = null;
        
            try {
                console.log('Updated profile before modification:', updatedProfile);

                // Atualiza o `username` com base no `email` antes de enviar ao servidor
                updatedProfile.username = updatedProfile.email;

                const response = await axios.put(
                    `${api}/api/users/${this.profile.email}`,
                    updatedProfile, 
                    {
                    withCredentials: true,
                });
        
                // Atualizar os dados locais
                this.completeProfile = response.data;
                console.log('Profile updated:', this.completeProfile);
            } catch (error) {
                this.error = 'Failed to update profile.';
                console.error(error);
            } finally {
                this.loading = false;
            }
        },
        
        // async getCompleteProfile() {
        //     this.loading = true;
        //     this.error = null;
        
        //     try {

        //         if (!this.profile.email) {
        //             this.error = 'Profile email is missing.';
        //             return;
        //         }
                
        //         // Faz a requisição GET para obter as informações do perfil completo
        //         const response = await axios.get(`http://localhost:3005/users/${this.profile.email}`);
        //         // const response = await axios.get(`${api}/api/users/${this.profile.email}`);

        //         // const response = await axios.get(
        //         //     `${api}/api/users/${this.profile.email}`,
        //         //     {
        //         //     withCredentials: true,
        //         // });
        
        //         // Atualiza o estado com os dados recebidos
        //         const completeProfile = response.data;
        
        //         console.log('Complete profile fetched:', completeProfile);
        
        //         // Atualizar o perfil no estado (ajuste conforme necessário)
        //         this.profile = {
        //             ...this.profile, // Retém as informações atuais
        //             ...completeProfile // Substitui pelos dados completos
        //         };
        //     } catch (error) {
        //         this.error = 'Failed to fetch complete profile.';
        //         console.error(error);
        //     } finally {
        //         this.loading = false;
        //     }
        // },


        async updatePassword(currentPassword, newPassword) {
            this.loading = true;
            this.error = null;

            try {
                // Verificação da senha atual e atualização da senha
                if (currentPassword !== this.profile.password_hash) {
                    this.error = 'Incorrect current password.';
                    return;
                }

                // Aqui você pode adicionar a lógica de hashing da nova senha antes de armazená-la
                const newPasswordHash = newPassword; // Simule o hashing aqui (ex: bcrypt)

                // Atualizando o perfil com a nova senha
                this.profile.password_hash = newPasswordHash;

                console.log('Password updated successfully!');
            } catch (error) {
                this.error = 'Failed to update password.';
                console.error(error);
            } finally {
                this.loading = false;
            }
        }
    },

    getters: {
        displayName: (state) => {
            return state.profile.fullName || state.profile.username || 'Anonymous User';
        }
    }
});
