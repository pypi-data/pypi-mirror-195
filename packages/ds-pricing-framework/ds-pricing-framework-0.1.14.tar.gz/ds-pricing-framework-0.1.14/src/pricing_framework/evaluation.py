"""
author: Kelsey Messonnier
email:  kelsey@just.insure
date:   27 January 2023
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tabulate as tb

class EvaluateFactor(object):
    """ Class for Graph Functions """

    
    def __init__(self,
                 df: "pd.DataFrame",
                 proposed_factor,
                 current_sort_by_var,
                 proposed_sort_by_var,
                 group_by_var,
                 number_of_groups,
                 curr_prem,
                 prop_prem,
                 il,
                 lift_title,
                 lift_xaxis_title,
                 lift_y1axis_title,
                 gini_title
                ):
        
        """
        :param df: dataframe
        :param current_sort_by_var: what you want to sort the charts by, for current way of doing things (ex: current ppm)
        :param current_sort_by_var: what you want to sort the charts by, for proposed way of doing things (ex: proposed ppm)
        :param group_by_var: what you want to group the charts by (ex: lifetime miles, premium, policy count)
        :param number_of_groups: how many groups you'd like to split by (ex: decile, quartile)
        :param curr_prem: current earned premium
        :param prop_prem: proposed earned premium after the change
        :param il: incurred losses
        :param lift_title: title for lift charts
        :param lift_xaxis_title: label for x axis 
        :param lift_y1axis_title: label for y axis (ex: decile, quartile)
        :param gini_title: title for lorenz curve
        """

        self.df = df
        self.proposed_factor = proposed_factor
        self.current_sort_by_var = current_sort_by_var
        self.proposed_sort_by_var = proposed_sort_by_var
        self.group_by_var = group_by_var
        self.number_of_groups = number_of_groups
        self.curr_prem = curr_prem
        self.prop_prem = prop_prem
        self.il = il
        self.title = lift_title
        self.xaxis_title = lift_xaxis_title
        self.y1axis_title = lift_y1axis_title
        self.gini_title = gini_title

        
    def lift_comparison(self):

        df = self.df
        
        total_group = df[self.group_by_var].sum()
        each_group = round(total_group/self.number_of_groups)

        x_list=[]
        y_list=[]

        groups = self.number_of_groups
        number = 0
        while number < groups+1:
            splits = each_group*(number)
            x_list.append(splits)
            number = number+1

        groups = self.number_of_groups
        number = 1
        while number <= groups:
            y_list.append(number)
            number = number+1
        y_array = np.array(y_list)


        #########################
        #        CURRENT        #
        ######################### 
        np.random.seed(42)
        df['rand'] = np.random.randint(1, 12, size=len(df))

        df_sorted = df.sort_values(by = [self.current_sort_by_var,'rand'], ascending=False)
        df_sorted['running_total'] = df_sorted[self.group_by_var].cumsum() 

        df_sorted['current_group'] = pd.cut(df_sorted["running_total"], x_list, labels = y_array)
        df_sorted.drop(columns=['rand','running_total'])


        #########################
        #        PROPOSED       #
        #########################
        df_sorted = df_sorted.sort_values(by = [self.proposed_sort_by_var,'rand'], ascending=False)
        df_sorted['running_total'] = df_sorted[self.group_by_var].cumsum() 

        df_sorted['proposed_group'] = pd.cut(df_sorted["running_total"], x_list, labels = y_array)
        df_sorted.drop(columns=['rand','running_total'])
        df = df_sorted


        ##############################
        #        CREATE CHARTS       #
        ##############################    
        df['ep1'] = self.curr_prem
        df['ep2'] = self.prop_prem
        total_loss_cost_per_day = df['total_incurred_losses'].sum()/df['lifetime_active_days'].sum()

        loss_cost_per_decile1 = df.groupby(['current_group'])['total_incurred_losses'].sum()
        miles_per_decile1 = df.groupby(['current_group'])['lifetime_active_days'].sum()
        lc1 = (loss_cost_per_decile1/miles_per_decile1)/total_loss_cost_per_day

        loss_cost_per_decile2 = df.groupby(['proposed_group'])['total_incurred_losses'].sum()
        miles_per_decile2 = df.groupby(['proposed_group'])['lifetime_active_days'].sum()
        lc2 = (loss_cost_per_decile2/miles_per_decile2)/total_loss_cost_per_day 

        feature_count1 = df.groupby(['current_group'])['feature_count'].sum()
        claim_count1 = df.groupby(['current_group'])['claim_count'].sum()
        lc_error1 = lc1/np.sqrt(claim_count1)

        feature_count2 = df.groupby(['proposed_group'])['feature_count'].sum()
        claim_count2 = df.groupby(['proposed_group'])['claim_count'].sum()
        lc_error2 = lc2/np.sqrt(claim_count2)

        loss_cost_per_decile1 = df.groupby(['current_group'])['total_incurred_losses'].sum()
        earned_prem_per_decile1 = df.groupby(['current_group'])['ep1'].sum()
        lr1 = (loss_cost_per_decile1/earned_prem_per_decile1)

        loss_cost_per_decile2 = df.groupby(['proposed_group'])['total_incurred_losses'].sum()
        earned_prem_per_decile2 = df.groupby(['proposed_group'])['ep2'].sum()
        lr2 = (loss_cost_per_decile2/earned_prem_per_decile2)

        feature_count1 = df.groupby(['current_group'])['feature_count'].sum()
        claim_count1 = df.groupby(['current_group'])['claim_count'].sum()
        lr_error1 = lr1/np.sqrt(claim_count1)

        feature_count2 = df.groupby(['proposed_group'])['feature_count'].sum()
        claim_count2 = df.groupby(['proposed_group'])['claim_count'].sum()
        lr_error2 = lr2/np.sqrt(claim_count2)

        fig, (ax1, ax2) = plt.subplots(1,2, figsize = (15,4))
        fig.suptitle(self.title)
        ax1.errorbar(y_list, 
                    lc1,
                    yerr=lc_error1,
                    capsize=4,label = "Current")
        ax1.errorbar(y_list,
                    lc2,
                    yerr=lc_error2,
                    capsize=4, label = "Proposed")
        ax1.set_title('Loss Cost Lift Curve')
        ax1.set_xlabel(self.xaxis_title)
        ax1.set_ylabel(self.y1axis_title)
        ax1.legend()

        # fig, ax = plt.subplots()
        ax2.errorbar(y_list,
                    lr1,
                    yerr=lr_error1,
                    capsize=4, label = 'Current')
        ax2.errorbar(y_list, 
                    lr2,
                    yerr=lr_error2,
                    capsize=4, label = 'Proposed')
        ax2.set_title('Loss Ratio Lift Curve')
        ax2.set_xlabel(self.xaxis_title)
        ax2.set_ylabel('Loss Ratio')
        ax2.legend()

        return plt.show()

    def gini_comparison(self):
    
        df = self.df
    
        #Rank the scores
        np.random.seed(42)
        df['rand'] = np.random.randint(1, 12, size=len(df))

        df_sorted_current = df.sort_values(by = [self.current_sort_by_var,'rand'], ascending=False)
        df_sorted_proposed = df.sort_values(by = [self.proposed_sort_by_var,'rand'], ascending=False)

        #Calculate Gini 1
        arr1 = np.array(df_sorted_current[self.il])
        count = arr1.size
        coefficient = 2 / count
        indexes = np.arange(1, count + 1)
        weighted_sum = (indexes * arr1).sum()
        total = arr1.sum()
        constant = (count + 1) / count
        gini_val1 = coefficient * weighted_sum / total - constant

        #Calculate Gini 2
        arr2 = np.array(df_sorted_proposed[self.il])
        count = arr2.size
        coefficient = 2 / count
        indexes = np.arange(1, count + 1)
        weighted_sum = (indexes * arr2).sum()
        total = arr1.sum()
        constant = (count + 1) / count
        gini_val2 = coefficient * weighted_sum / total - constant

        #Lorenz Curve 1
        X_lorenz1 = arr1.cumsum() / arr1.sum()
        X_lorenz1 = np.insert(X_lorenz1, 0, 0) 
        X_lorenz1[0], X_lorenz1[-1]

        #Lorenz Curve 2
        X_lorenz2 = arr2.cumsum() / arr2.sum()
        X_lorenz2 = np.insert(X_lorenz2, 0, 0) 
        X_lorenz2[0], X_lorenz2[-1]

        #Graph it
        fig, ax = plt.subplots(figsize=[6,6])
        ax.plot(np.arange(X_lorenz1.size)/(X_lorenz1.size-1), X_lorenz1, label = "Current: Gini = %.4f" %(gini_val1))
        ax.plot(np.arange(X_lorenz2.size)/(X_lorenz2.size-1), X_lorenz2, label = "Proposed: Gini = %.4f" %(gini_val2))
        ax.plot([0,1], [0,1], '--', color='k')
        plt.title(self.gini_title)
        plt.legend()

        return plt.show()

    def compare_loss_table(self):
    
        df = self.df
        proposed_variable = self.proposed_factor
    
        variable = df[proposed_variable].unique()
        variable = variable.tolist()
        variable.sort()
        count = df.groupby([proposed_variable])["policy_number"].count()
        claim = df.groupby([proposed_variable])["claim_indicator"].sum()
        freq = claim/count

        il = df.groupby([proposed_variable])["il"].sum()
        curr_ep = df.groupby([proposed_variable])["curr_earned_premium"].sum()
        prop_ep = df.groupby([proposed_variable])["prop_earned_premium"].sum()
        curr_lr = il/curr_ep
        prop_lr = il/prop_ep

        titles = [proposed_variable, 'Policy Count', '# of Claims', 'Freq.', 'Current LR', 'Proposed LR']
        rows = list(zip(variable, count, claim, freq, curr_lr, prop_lr))

        return print(tb.tabulate(rows, headers=titles, floatfmt=".4f"))
    
    def overall_impact(self):

        df = self.df
        
        df2 = df[df.curr_price_per_mile != df.prop_price_per_mile]

        count = df2["policy_number"].count()
        total_plcy_count = df["policy_number"].count()
        pct_impacted = count/total_plcy_count

        curr_prem = df["curr_earned_premium"].sum()
        prop_prem = df["prop_earned_premium"].sum()
        pct_change_prem = (prop_prem - curr_prem)/curr_prem

        curr_ppm2 = df2["curr_price_per_mile"].mean()
        prop_ppm2 = df2["prop_price_per_mile"].mean()
        pct_change_ppm2 = (prop_ppm2 - curr_ppm2)/curr_ppm2

        curr_ppm = df["curr_price_per_mile"].mean()
        prop_ppm = df["prop_price_per_mile"].mean()
        pct_change_ppm = (prop_ppm - curr_ppm)/curr_ppm

        il = df["il"].sum()
        curr_lr = il/curr_prem
        prop_lr = il/prop_prem

        print('                    Current         Proposed           % Change')

        print('\nPolicies Impacted:  0', end= '               ')
        print('{:,}'.format(count), end = '              ')
        print('{:.2f}%'.format(pct_impacted*100))

        print('\nImpacted Avg PPM:   {:,.2f}'.format(curr_ppm2), end = '           ')
        print('{:,.2f}'.format(prop_ppm2), end = '              ')
        print('{:.2f}%'.format(pct_change_ppm2*100))

        print('\nTotal Avg PPM:      {:,.2f}'.format(curr_ppm), end = '           ')
        print('{:,.2f}'.format(prop_ppm), end = '              ')
        print('{:.2f}%'.format(pct_change_ppm*100))

        print('\nTotal Prem Change:  {:,.0f}'.format(curr_prem), end = '       ')
        print('{:,.0f}'.format(prop_prem), end = '          ')
        print('{:.2f}%'.format(pct_change_prem*100))

        print('\nTotal Loss Ratio:   {:.2f}%'.format(curr_lr*100), end= '          ')
        print('{:,.2f}%'.format(prop_lr*100), end = '             ')
        print('{:.2f}%'.format((prop_lr-curr_lr)/curr_lr*100))

    def run_eval(self):
        self.lift_comparison()
        self.gini_comparison()

    def run_impact(self):
        self.compare_loss_table()
        self.overall_impact()

    def __str__(self):
        return f'{self.name}={self.value}'
    
