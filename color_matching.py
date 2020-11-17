# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 18:15:23 2020

@author: malrawi


"""
from color_table import ColorTable
import pickle
import numpy as np
from distance_troch import euclidean_distance # , cosine_similarity_n_space
import itertools
from generate_colors import generate_pack_of_colors

class ColorMatching():
    ''' Arranges colors of fashion/clothing items into a pandas table. 
    Each outfit is stored into a single table. Tables of several outfits can be appended '''
    def __init__(self):
        
        self.ref_data_dict = None                  
   
    def load(self, fname, path = 'C:/MyPrograms/FashionColor/ColorFiles/'):   
        with open(path+fname, 'rb') as fp:
            self.ref_data_dict = pickle.load(fp)
   
    def all_query_items_exist(self, items_to_match, query_items): 
        ''' Returns False if not all items to match are in ref_items, else returns True '''
                
        return set(items_to_match).issubset(query_items)
            
            
    
    def get_image_names(self, obj): # example: clothing_item = 'jacket'       
        return list(obj.data_dict['colr_df'].keys())
    
    
    
    def to_2D_mat(self, obj, img_name, item, dict_name):
        'Converts the color to a 2D matrix; output is RGB x NoColros'
        c_vals = obj.data_dict[dict_name][img_name].loc[item].values                 
        c_vals = np.reshape(c_vals, (c_vals.shape[0], -1))
        c_vals = np.vstack(c_vals[:, 0]).astype(np.float) # now, torch.tensor(aa) is OK
        return c_vals
    
    def remove_nans_from_numpy(self, inp):
        ''' Removing nan's from a numpy array, will always return a 1D array 
        even if the input is 2D or 3D '''
        return inp[~np.isnan(inp)] # return inp[~np.isnan(inp).any(axis=1)] # this keeps the 2D structure
        
                

    
    def sort_and_store_record(self, dist_metric, catalogue_name, num_best_maches):
        ' Stores and sorts the results using the distance values'
        result = {}     
        result['dist_metric'] = dist_metric
        result['catalogue_name'] = catalogue_name 
        result['info'] = [] # to be appended with info
                                
        # sorting records according to distance                           
        idx_sorted_dist = np.argsort(result['dist_metric'])        
        result['catalogue_name'] = [result['catalogue_name'][i] for i in idx_sorted_dist]
        result['dist_metric'] = [result['dist_metric'][i] for i in idx_sorted_dist]
        
        # selecting the num of best matches
        result['dist_metric'] = result['dist_metric'][:num_best_maches]
        result['catalogue_name'] = result['catalogue_name'][:num_best_maches]   
        self.remove_dublicates(result) # removal of duplicates has to be done after the soreting, as we don't want to remove low distacne matches
        return result 
   
       
            
    def get_colors_from_results(r_obj, result):
        ''' TODO '''
        for i in range(len(result['catalogue_name'])):
            query = result['catalogue_name'][i]['query'] # in the future, this should be a list of images, for each of the matched_items
            color_mathces_catalogue_name = result['catalogue_name'][i]['reference']
            matched_items = result['catalogue_name'][i]['matched_items']
                            
        return 0
        
    
              
    def find_e_distance_new(self, c_ref, p_ref, c_query, p_query, n_val=0 ):
        ''' $$e_{ij}(\text{s(group)}, \text{ground_truth}) = \frac{|p_i*P_j| |a_i - A_j|}{(p_i+P_j)^n}
            
            e_{ij}(\text{s(group)}, \text{ground_truth}) = \frac{|p_i*P_j| |a_i - A_j|}{(p_i+P_j)^n}
            $$            
            # if we want to test with 0s instead of nans
            # c_ref = np.nan_to_num(c_ref, 0)
            # p_ref = np.nan_to_num(p_ref, 0)
            # c_query = np.nan_to_num(c_query, 0)
            # p_query= np.nan_to_num(p_query, 0)
        
               '''
        
        # we need to make sure c_ref and c_query are of the same size, do embedding otherwise  
        
        # rgb_out = rgb_in.copy()
        # rgb_out.fill(np.nan)
        
        ''' IMPORTANT
        We may not need nans or 0 padded AT ALLL
        
        '''        
        c_ref = self.remove_nans_from_numpy(c_ref)
        c_query = self.remove_nans_from_numpy(c_query)
        dist_clr = euclidean_distance(c_ref, c_query)
                
        p_query = p_query[~np.isnan(p_query)]
        p_ref = p_ref[~np.isnan(p_ref)]
                
        prob_mult  = (p_ref.reshape(-1,1) * p_query) 
        prob_mult = self.remove_nans_from_numpy(prob_mult) 
        
        return np.mean(dist_clr*prob_mult) # this is problematic, if the idstance of probability is zero, and the color is wrong, it will give 0 ...meaning perfecct color match, which is wrong
                
    def find_e_distance(self, c_ref, p_ref, c_query, p_query, n_val=0 ):
        ''' $$e_{ij}(\text{s(group)}, \text{ground_truth}) = \frac{|p_i*P_j| |a_i - A_j|}{(p_i+P_j)^n}
            
            e_{ij}(\text{s(group)}, \text{ground_truth}) = \frac{|p_i*P_j| |a_i - A_j|}{(p_i+P_j)^n}
            $$            
            # if we want to test with 0s instead of nans
            # c_ref = np.nan_to_num(c_ref, 0)
            # p_ref = np.nan_to_num(p_ref, 0)
            # c_query = np.nan_to_num(c_query, 0)
            # p_query= np.nan_to_num(p_query, 0)
        
               '''
        
        # we need to make sure c_ref and c_query are of the same size, do embedding otherwise  
        
        # rgb_out = rgb_in.copy()
        # rgb_out.fill(np.nan)
        
        ''' IMPORTANT
        We may not need nans or 0 padded AT ALLL
        
        '''        
        dist_clr = euclidean_distance(c_ref, c_query)
        dist_clr = self.remove_nans_from_numpy(dist_clr)        
        
        prob_mult  = (p_ref.reshape(-1,1) * p_query) 
        prob_mult = self.remove_nans_from_numpy(prob_mult) 

        
        return np.mean(dist_clr*prob_mult) # this is problematic, if the idstance of probability is zero, and the color is wrong, it will give 0 ...meaning perfecct color match, which is wrong


        
    def generage_item_pairs(self, items_to_match, wardrobe_obj):
        ''' Returns all the items as pairs, or triplets, depending on the number of items in
        items_to_match. For example, if we have "shirt" and "pants", then, 
        this function returns all the images of the wardrobe that has "shirt" and "pants", like
        ("shirt1", "pants1"  ),("shirt2", "pants2"  ), and so on  '''
        query_img_names = []        
        for item in items_to_match:
                query_img_names.append(wardrobe_obj.data_dict['pix_cnt_df'][item].index.tolist())
        if len(query_img_names)==2:
            item_pairs = list(itertools.product(query_img_names[0],query_img_names[1]))
        elif len(query_img_names)==3:
            item_pairs = list(itertools.product(query_img_names[0],query_img_names[1],query_img_names[2] ))
        elif len(query_img_names)==4:
            item_pairs = list(itertools.product(query_img_names[0],query_img_names[1],query_img_names[2], query_img_names[3] ))
        elif len(query_img_names)==5:
            item_pairs = list(itertools.product(query_img_names[0],query_img_names[1],query_img_names[2], query_img_names[3], query_img_names[4] ))
        
        return item_pairs
       
    def remove_dublicates(self, result): 
        '''Two, or more, might be identified as matches 
        
         Removal of duplicates has to be done after the soreting, as we don't want to remove low distacne matches
        '''
        z = result['catalogue_name']
        dublicate_idx = []
        for i in range(len(z)):
            for j in range(i+1, len(z)):
                if z[i]['matched_items']==z[j]['matched_items']:                       
                    dublicate_idx.append(j)
                    i=i-1
                    break
        cnt = 0            
        for j in sorted(dublicate_idx):
            result['catalogue_name'].pop(j-cnt)
            result['dist_metric'].pop(j-cnt)            
            cnt +=1            
            # print(j)
        if cnt>0:
            print()
            result['info'].append('dublicate matches removed')
                    
    
        
    
    def user_wardrobe_v_ref_matches(self, ref_obj, wardrobe_obj, items_to_match = ['jacket', 'pants', 'shirt' ], 
                  n_val=0.5, num_best_maches = 10): 
            '''  query_obj should contain clothing from  one person's wardrob and we find the best match after comparing it
            to the ref_obj (which is something like the trend catalogue) 
            
            -n_val: used to control the probability normalization, in case we have
            low probablities of some color making the distance low. The n_val 
            penalizes low probabilities 
            
            output
            - result: a dictionary that contains the matches and the distances 
            
            What is a wordrobe? A wardrobe is a collection of single-item images,
            that is, eacah image has just one single item. These collections
            are stored in a folder named by the user_name            '''        
            
            self.wardrobe_sanity_check(wardrobe_obj, items_to_match)
                                   
            dist_metric = [];  catalogue_name = []
            print('matching according to', ref_obj.data_dict['obj_name'], 'catalogue' )                        
            item_pairs = self.generage_item_pairs(items_to_match, wardrobe_obj)              
                
            for ref_img_name in self.get_image_names(ref_obj):
                ref_items  = list(ref_obj.data_dict['pix_cnt_df'][ref_img_name].index) # this does not work in debug mode, but ok in run mode
                ''' we need to check of items_to_match in wardrobe_iems '''
                if not self.all_query_items_exist(items_to_match, ref_items): continue
                print('Image with', items_to_match, 'is:', ref_img_name)  
                               
            
                for item_pair in item_pairs:
                    dist_item = 0
                    for query_img_name in item_pair:
                        item = query_img_name[:query_img_name.find('_')]                         
                        p_ref = ref_obj.data_dict['pix_cnt_df'][ref_img_name].loc[item].values
                        c_ref = self.to_2D_mat(ref_obj, ref_img_name, item, 'colr_df')
                        p_query = wardrobe_obj.data_dict['pix_cnt_df'][item].loc[query_img_name].values # for the wardrobe, the image_name is used instead of the item in the pandas table
                        c_query = self.to_2D_mat(wardrobe_obj, item, query_img_name, 'colr_df')

                        dist_item += self.find_e_distance(c_ref, p_ref, c_query, p_query, n_val )                        
                                                
                    dist_metric.append(dist_item) # much easier to store the distance separately, as we need it to find the min values to obtain the best matches
                    catalogue_name.append({'matched_items': item_pair, 'query':items_to_match,  'reference': ref_img_name }) # registering the catalogue that possibly matches the query
                
            result  = self.sort_and_store_record(dist_metric,catalogue_name, num_best_maches)
            result['info'].append(ref_obj.data_dict['obj_name'])
            
            
            return result

    
    def wardrobe_sanity_check(self, wardrobe_obj, items_to_match):
        items_to_match = [items_to_match] if not isinstance(items_to_match, list) else items_to_match # if the input is not a list, make it a list
        if len(items_to_match)<2: 
            print('Error: there is less than 2 items to match, min items should be 2')
            exit()
       
        wardrobe_items = self.get_image_names(wardrobe_obj) # here, we get the labels and not the image names, since we've restructured the wardrobe
        if not self.all_query_items_exist(items_to_match, wardrobe_items):                           
            print('Wardrobe does not have all items to match, these are:', items_to_match)
            print('Wardrobe, on the other hand, has only these labels:', wardrobe_items)
            exit()
            
        return True
    
    
    
    
    def get_color_pack(self, rgb_in, p_in, n_split, mode = 'complement'):

        '''     now, it is possible that c_1_orig has more than one RGB value 
                we need to deal with it. Two approaches:
                    1- use n_split>0 for each RGB, and consider each RGB separately
                    2- use low n_split (0,1) and merge both RGBs into one structure            
        '''
        
        for i, rgb_val in enumerate(rgb_in):
            if np.isnan(rgb_val).any():
                break
            color_pack = generate_pack_of_colors(rgb_val, n_split= n_split, p0=p_in[i], mode = mode )   # ''' - normal uses only complement and analogous - colorful uses oppsite and shade  '''
             
        return color_pack
    
    
        
    def user_wardrobe_vs_itself_matches(self, wardrobe_obj, items_to_match = ['jacket', 'pants', 'shirt' ], 
                  n_val=0.5, num_best_maches = 10, n_split=1):
        dist_metric = []; catalogue_name = []
        self.wardrobe_sanity_check(wardrobe_obj, items_to_match)        
        
        for item_ref in items_to_match: # this mainly has one item, but did a for-loop for generality                
            for ref_img_name in wardrobe_obj.data_dict['colr_df'][item_ref].index:
                p_ref = wardrobe_obj.data_dict['pix_cnt_df'][item_ref].loc[ref_img_name].values # for the wardrobe, the image_name is used instead of the item in the pandas table
                c_ref = self.to_2D_mat(wardrobe_obj, item_ref, ref_img_name, 'colr_df')       
                items_to_match_minus_ref = items_to_match.copy()   
                items_to_match_minus_ref.remove(item_ref) # we are comparing each piece in item with the rest of items in items_to_match            
                # generate the colors of every query_image_name, then, find the distance with each single item
                for item_query in items_to_match_minus_ref:                     
                    for query_img_name in wardrobe_obj.data_dict['colr_df'][item_query].index:                        
                        p_query_orig = wardrobe_obj.data_dict['pix_cnt_df'][item_query].loc[query_img_name].values # for the wardrobe, the image_name is used instead of the item in the pandas table
                        c_query_orig = self.to_2D_mat(wardrobe_obj, item_query, query_img_name, 'colr_df')
                        # now, we have to change the color of c_query (or c1)
                        query_color_pack = self.get_color_pack(c_query_orig, 
                                                               p_query_orig, n_split, mode = 'complement') # we have to take the effect of the original probability and multiply it by the new one from the split, necessary when c_query_orig has more than one RGB with different probabilities
                                                
                        for c_query_key in query_color_pack:                             
                            ''' we need a distance for each pack, one for complement, one for analogous, etc... 
                            so, no need for the for-loop here '''
                            if c_query_key == 'num_split': continue # this is not key, but split num / information                            
                            c_query_instance = query_color_pack[c_query_key]['color']                            
                            p_query_instance = query_color_pack[c_query_key]['prob'] # this is the resutlant split probabilit multiplied by the prior p0=p_query_orig, that is, low values p_query_orig should penalize the new colors                                    
                            dist_item = self.find_e_distance(c_query_instance, 
                                                              p_query_instance, 
                                                              c_ref, p_ref)  
                            dist_metric.append(dist_item) # much easier to store the distance separately, as we need it to find the min values to obtain the best matches
                            catalogue_name.append({'query': items_to_match, 
                                                   'reference': 'Self Wardrobe', 
                                                   'matched_items': (query_img_name, ref_img_name),
                                                   'color-match': c_query_key
                                                   }) # registering the catalogue that possibly matches the query
                                                     
                        
        result = self.sort_and_store_record(dist_metric, catalogue_name, num_best_maches)
        result['info'].append(wardrobe_obj.data_dict['obj_name'])        
        return result

        
    
    def ref_v_ref_matches(self, ref_obj, query_obj, items_to_match = ['jacket', 'pants', 'shirt' ], 
              n_val=0.5, num_best_maches = 10): 
        '''  query_obj should contain clothing from whole person (outfit) and we find the best match 
        after comparing it to other outfits stored in ref_obj (which is something like the trend catalogue) 
        
        -n_val: used to control the probability normalization, in case we have
        low probablities of some color making the distance low. The n_val 
        penalizes low probabilities 
        
        output
        - result: a dictionary that contains the matches and the distances '''        
        
        items_to_match = [items_to_match] if not isinstance(items_to_match, list) else items_to_match
        print('matching according to', ref_obj.data_dict['obj_name'], 'catalogue' )              
        
        ref_images = self.get_image_names(ref_obj)
        query_images = self.get_image_names(query_obj)
        
         
        dist_metric = []
        catalogue_name = []
        
        for ref_img_name in ref_images:
            ref_items  = list(ref_obj.data_dict['pix_cnt_df'][ref_img_name].index)
            if not self.all_query_items_exist(items_to_match, ref_items): continue
            for query_img_name in query_images:
                query_items  = list(query_obj.data_dict['pix_cnt_df'][query_img_name].index)
                if not self.all_query_items_exist(items_to_match, query_items): continue
                
                dist_item = 0
                for item in items_to_match:                 
                    p_ref = ref_obj.data_dict['pix_cnt_df'][ref_img_name].loc[item].values            
                    c_ref = self.to_2D_mat(ref_obj, ref_img_name, item, 'colr_df')
                    
                    p_query = query_obj.data_dict['pix_cnt_df'][query_img_name].loc[item].values            
                    c_query = self.to_2D_mat(query_obj, query_img_name, item, 'colr_df')
                    
                    
                    dist_item += self.find_e_distance(c_ref, p_ref, c_query,p_query, n_val )
                
                dist_metric.append(dist_item) # much easier to store the distance separately, as we need it to find the min values to obtain the best matches
                catalogue_name.append({'query':query_img_name, 'reference': ref_img_name, 'matched_items': items_to_match}) # registering the catalogue that possibly matches the query
        
        result = self.sort_and_store_record(dist_metric, catalogue_name, num_best_maches)
        result['info'].append(ref_obj.data_dict['obj_name'])
        return result



x = ColorMatching()
catalogue = 'ref_clothCoP'
ref_obj = ColorTable(fashion_obj_name='Catalogue '+catalogue) 
ref_obj.load('ref_clothCoP.pkl')

wardrobe_user_name = 'malrawi'
user_obj = ColorTable(fashion_obj_name = 'Wardrobe of '+ wardrobe_user_name) 
user_obj.load( wardrobe_user_name +'.pkl')


items_to_match = ['jacket', 'pants']
# result = x.ref_v_ref_matches(ref_obj, user_obj, items_to_match, n_val=0.5, num_best_maches = 4)
# result = x.user_wardrobe_v_ref_matches(ref_obj, user_obj, 
#                                         items_to_match, n_val=0.5, 
#                                         num_best_maches = 10)

result = x.user_wardrobe_vs_itself_matches(user_obj, 
                                        items_to_match, 
                                        n_val=0.5, 
                                        num_best_maches = 10, 
                                        n_split = 0)


        

#  ------ Old  --- -- - - --
# dist_prob = euclidean_distance(p_ref.reshape(-1,1), p_query.reshape(-1,1)) # resahpe needed as cdist only accepts 2D tensors
# dist_prob = self.remove_nans_from_numpy(dist_prob)                    
# prob_sum  = (p_ref.reshape(-1,1) + p_query)**n_val          
# prob_sum = self.remove_nans_from_numpy(prob_sum)

# return np.mean(dist_clr*dist_prob/(prob_sum + 1e-20))  # 
# return np.sum(dist_clr*dist_prob/(prob_sum )) # this is problematic, if the idstance of probability is zero, and the color is wrong, it will give 0 ...meaning perfecct color match, which is wrong
# return np.mean(dist_clr*(dist_prob + prob_sum)) # this is problematic, if the idstance of probability is zero, and the color is wrong, it will give 0 ...meaning perfecct color match, which is wrong
